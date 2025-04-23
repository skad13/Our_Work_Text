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
    description = models.TextField(blank=True)
    travel_agency = models.ForeignKey('TravelAgency', on_delete=models.CASCADE, related_name='routes')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RoutePoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points')
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.route.name} - {self.name}"


class PointImage(models.Model):
    point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='point_images/')

    def __str__(self):
        return f"{self.point.name} - Image {self.id}"


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
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
        ('waitlist', '候补'),
    ]

    tourist = models.ForeignKey('Tourist', on_delete=models.CASCADE, related_name='bookings')
    itinerary = models.ForeignKey('Itinerary', on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, null=True)  # 候补预订时的申请理由
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tourist.user.username} - {self.itinerary.route.name} - {self.status}"

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class GuideSalary(models.Model):
    guide = models.OneToOneField(Guide, on_delete=models.CASCADE, related_name='salary')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 团队提成百分比
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guide.user.username}'s Salary"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatRoomMember(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms')
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} in {self.room.name}"