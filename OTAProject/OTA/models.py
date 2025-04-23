# OTAProject/OTA/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('tourist', '游客'),
        ('guide', '导游'),
        ('travel_agency', '旅行社'),
        ('tourism_bureau', '文旅局'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    # 解决related_name冲突问题
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='ota_user_groups',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='ota_user_permissions',
        related_query_name='user',
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'ota_user'


class TravelAgency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='travel_agency')
    agency_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.agency_name

    class Meta:
        verbose_name = '旅行社'
        verbose_name_plural = '旅行社'


class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guide')
    guide_id = models.CharField(max_length=50)
    travel_agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE, related_name='guides')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '导游'
        verbose_name_plural = '导游'


class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tourist')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '游客'
        verbose_name_plural = '游客'


class Route(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    travel_agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE, related_name='routes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RoutePoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points')
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.route.name} - {self.name}"


class PointImage(models.Model):
    point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='route_points/')

    def __str__(self):
        return f"Image for {self.point.name}"


class Itinerary(models.Model):
    STATUS_CHOICES = (
        ('active', '进行中'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    )

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='itineraries')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True, related_name='itineraries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    max_tourists = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.route.name} - {self.start_date}"

    class Meta:
        verbose_name = '行程'
        verbose_name_plural = '行程'


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
    )

    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE, related_name='bookings')
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist.user.username} - {self.itinerary.route.name}"

    class Meta:
        verbose_name = '预订'
        verbose_name_plural = '预订'


class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('rejected', '已驳回'),
    )

    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE, related_name='complaints')
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='complaints', null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tourist.user.username} - {self.title}"