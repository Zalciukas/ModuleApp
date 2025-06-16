from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
import datetime

from .models import Module
from .forms import ModuleForm

class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    template_name = 'modules/module_list.html'
    context_object_name = 'modules'
    paginate_by = 10
    
    def get_queryset(self):
        return Module.objects.filter(user=self.request.user).order_by('-s', 'subject_name_english') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modules = self.get_queryset()
        context['total_modules'] = modules.count()
        context['total_credits'] = sum(m.credits_received for m in modules)
        context['avg_credits'] = context['total_credits'] / context['total_modules'] if context['total_modules'] > 0 else 0
        return context

class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'modules/module_form.html'
    success_url = reverse_lazy('modules:list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Module created successfully!')
        return super().form_valid(form)

class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = 'modules/module_form.html'
    success_url = reverse_lazy('modules:list')
    
    def get_queryset(self):
        return Module.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Module updated successfully!')
        return super().form_valid(form)

class ModuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Module
    template_name = 'modules/module_confirm_delete.html'
    success_url = reverse_lazy('modules:list')
    
    def get_queryset(self):
        return Module.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Module deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def generate_modules_pdf(request):
    """Generate PDF report of all user's modules"""
    modules = Module.objects.filter(user=request.user).order_by('-s', 'subject_name_english') 
    
    if not modules.exists():
        messages.warning(request, 'No modules found to generate PDF.')
        return HttpResponse("No modules found", status=404) 
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*72, bottomMargin=1*72)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    # Build PDF content
    elements = []
    
    # Title
    title = Paragraph(f"Module Report - {request.user.get_full_name()}", title_style)
    elements.append(title)
    
    # Summary info
    total_credits = sum(m.credits_received for m in modules)
    summary_text = f"Total Modules: {modules.count()} | Total Credits: {total_credits} | Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    summary = Paragraph(summary_text, styles['Normal'])
    elements.append(summary)
    elements.append(Spacer(1, 20))
    
    # Create table data
    data = [['Semester', 'Subject (English)', 'University', 'Language', 'Credits', 'Grade', 'Level']]
    
    for module in modules:
        data.append([
            f"S{module.s}",
            module.subject_name_english[:40] + ('...' if len(module.subject_name_english) > 40 else ''),
            module.am[:20] + ('...' if len(module.am) > 20 else ''),
            module.get_language_display(),
            str(module.credits_received),
            module.grade or '-',
            module.get_level_achieved_display() or '-'
        ])
    
    # Create and style table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data styling
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightblue]),
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    
    # Return PDF response
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="modules_report_{request.user.username}.pdf"'
    
    return response