from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Module(models.Model):
    LANGUAGE_CHOICES = [
        ('LT', 'Lithuanian'),
        ('EN', 'English'),
        ('DE', 'German'),
        ('FR', 'French'),
        ('ES', 'Spanish'),
    ]
    
    SELECTION_TYPE_CHOICES = [
        ('MANDATORY', 'Mandatory'),
        ('ELECTIVE', 'Elective'),
        ('FREE_ELECTIVE', 'Free Elective'),
    ]
    
    ASSESSMENT_FORM_CHOICES = [
        ('EXAM', 'Exam'),
        ('ASSESSMENT', 'Assessment'), 
        ('PROJECT', 'Project'),
        ('PRESENTATION', 'Presentation'),
    ]
    
    STUDY_PART_CHOICES = [
        ('BACHELOR', 'Bachelor'),
        ('MASTER', 'Master'),
        ('DOCTORAL', 'Doctoral'),
    ]
    
    LEVEL_ACHIEVED_CHOICES = [
        ('A', 'A (Excellent)'),
        ('B', 'B (Good)'),
        ('C', 'C (Satisfactory)'),
        ('D', 'D (Poor)'),
        ('F', 'F (Fail)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modules')
    
    # Basic Information
    s = models.PositiveIntegerField(
        verbose_name="Semester",
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    am = models.CharField(max_length=100, verbose_name="University")
    subject_name_lithuanian = models.CharField(max_length=200, verbose_name="Subject Name (Lithuanian)")
    subject_name_english = models.CharField(max_length=200, verbose_name="Subject Name (English)")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, verbose_name="Language")
    selection_type = models.CharField(max_length=20, choices=SELECTION_TYPE_CHOICES, verbose_name="Selection Type")
    assessment_form = models.CharField(max_length=20, choices=ASSESSMENT_FORM_CHOICES, verbose_name="Assessment Form")
    study_part = models.CharField(max_length=20, choices=STUDY_PART_CHOICES, verbose_name="Study Part")
    
    # Credits and Hours
    planned_credits = models.PositiveIntegerField(
        verbose_name="Planned Credits",
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    hours = models.PositiveIntegerField(
        verbose_name="Hours",
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    credits_received = models.PositiveIntegerField(
        verbose_name="Credits Received",
        validators=[MinValueValidator(0), MaxValueValidator(30)]
    )
    
    # Grades
    original_grade = models.CharField(max_length=10, verbose_name="Original Grade", blank=True)
    original_credits = models.PositiveIntegerField(
        verbose_name="Original Credits",
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        null=True, blank=True
    )
    grade = models.CharField(max_length=10, verbose_name="Grade", blank=True)
    level_achieved = models.CharField(
        max_length=1, 
        choices=LEVEL_ACHIEVED_CHOICES, 
        verbose_name="Level Achieved",
        blank=True
    )
    
    # Dates
    exam_date = models.DateField(verbose_name="Exam Date", null=True, blank=True)
    registration_date = models.DateField(verbose_name="Registration Date", null=True, blank=True)
    
    # Teacher
    teacher = models.CharField(max_length=100, verbose_name="Teacher", blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-s', 'subject_name_english']
        verbose_name = "Module"
        verbose_name_plural = "Modules"
    
    def __str__(self):
        return f"S{self.s} - {self.subject_name_english}"
    
    def get_absolute_url(self):
        return reverse('modules:detail', kwargs={'pk': self.pk})