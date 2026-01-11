from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class ForumMessage(models.Model):
    CHANNEL_CHOICES = [
        ("general", "Allgemein"),
        ("projects", "Projekte"),
        ("offtopic", "Off-Topic"),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=32, choices=CHANNEL_CHOICES, default="general")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} [{self.get_channel_display()}]: {self.content[:40]}"


class YouthOrganization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    founded_date = models.DateField()
    location = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='youth_org_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.youthmember_set.count()


class YouthMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='youth_profile')
    organization = models.ForeignKey(YouthOrganization, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    school = models.CharField(max_length=200, blank=True)
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(13)],
        null=True,
        blank=True
    )
    parent_guardian_name = models.CharField(max_length=200)
    parent_guardian_phone = models.CharField(max_length=20)
    parent_guardian_email = models.EmailField()
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relation = models.CharField(max_length=100)
    skills = models.TextField(blank=True, help_text="List any skills or interests relevant to the organization")
    join_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.organization.name}"
    
    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    class Meta:
        ordering = ['user__last_name', 'user__first_name']
