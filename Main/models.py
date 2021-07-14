from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE


# 种类

class KIND(models.Model):
    KID = models.BigAutoField(primary_key=True, null=False)
    PKID = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True, verbose_name="父级种类")
    Name = models.CharField(max_length=15, verbose_name="种类名", unique=True)

    class Meta:
        db_table = 'KIND'
        verbose_name = '种类'

    def __str__(self):
        return self.Name


# 商户模型

class SHOPS(models.Model):
    class Type_CHOICE(models.IntegerChoices):
        PERSON = 0, '个人'
        ENTERPRISE = 1, '企业'

    SID = models.BigAutoField(primary_key=True, null=False)
    UID = models.OneToOneField(User, on_delete=models.RESTRICT, verbose_name="绑定的登录用户", null=True, blank=True)
    DES = models.TextField(verbose_name="商户的描述")
    Name = models.CharField(max_length=20, verbose_name="商户名称")
    Pic = models.ImageField(upload_to='productimg', verbose_name='商户Logo')
    KID = models.ForeignKey(KIND, on_delete=models.RESTRICT, verbose_name="主营商品类型")
    TYPE = models.IntegerField(choices=Type_CHOICE.choices, default=Type_CHOICE.PERSON, verbose_name="商户类型")

    class Meta:
        db_table = 'SHOP'
        verbose_name = '商户'

    def __str__(self):
        return self.Name


# 买家信息
class Customer(models.Model):
    STATE_CHOICES = (
        ('河北省', '河北省'),
        ('山西省', '山西省'),
        ('辽宁省', '辽宁省'),
        ('吉林省', '吉林省'),
        ('黑龙江省', '黑龙江省'),
        ('江苏省', '江苏省'),
        ('浙江省', '浙江省'),
        ('安徽省', '安徽省'),
        ('福建省', '福建省'),
        ('江西省', '江西省'),
        ('山东省', '山东省'),
        ('河南省', '河南省'),
        ('湖北省', '湖北省'),
        ('湖南省', '湖南省'),
        ('广东省', '广东省'),
        ('海南省', '海南省'),
        ('四川省', '四川省'),
        ('贵州省', '贵州省'),
        ('云南省', '云南省'),
        ('陕西省', '陕西省'),
        ('甘肃省', '甘肃省'),
        ('青海省', '青海省'),
        ('台湾省', '台湾省'),
        ('内蒙古自治区', '内蒙古自治区'),
        ('西藏自治区', '西藏自治区'),
        ('宁夏回族自治区', '宁夏回族自治区'),
        ('新疆维吾尔自治区', '新疆维吾尔自治区'),
        ('北京市', '北京市'),
        ('天津市', '天津市'),
        ('上海市', '上海市'),
        ('重庆市', '重庆市'),
    )
    id = models.BigAutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='登录名')
    name = models.CharField(max_length=200, verbose_name='姓名')
    locality = models.CharField(max_length=200, verbose_name='所在地')
    city = models.CharField(max_length=200, verbose_name='城市')
    zipcode = models.IntegerField(verbose_name='邮编')
    state = models.CharField(choices=STATE_CHOICES, max_length=20, verbose_name='省份')

    class Meta:
        verbose_name = '顾客信息'

    def __str__(self):
        return str(self.id)


# 商品信息
class Product(models.Model):
    class Status_CHOICE(models.IntegerChoices):
        NORMAL = 0, '正常浏览'
        NOT_SALE = 1, '商家下架'
        INVALID = 2, '违规下架'
    id = models.BigAutoField(primary_key=True, null=False)
    title = models.CharField(max_length=200, verbose_name='标题')
    selling_price = models.FloatField(verbose_name='销售价')
    discounted_price = models.FloatField(verbose_name='打折价')
    description = models.TextField(verbose_name='商品描述')
    kind = models.ForeignKey(KIND, on_delete=models.CASCADE, verbose_name='种类')
    product_image = models.ImageField(upload_to='productimg', verbose_name='商品图片')
    Status = models.IntegerField(choices=Status_CHOICE.choices, default=Status_CHOICE.NORMAL, verbose_name="商品可浏览性")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '商品'


# 购物车
class Cart(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='对应客户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='对应产品')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')

    class Meta:
        verbose_name = '购物车'

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


# 订单模型
class OrderPlaced(models.Model):
    class CHOICE(models.TextChoices):
        Accepted = '已完成', '已完成'
        Paked = '已打包', '已打包'
        OnWay = '已发货','已发货'
        Delivered = '已送达','已送达'
        Cancel = '已取消','已取消'
        pending = '受理中','受理中'
    id = models.BigAutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='对应用户')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='用户信息')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='购买商品')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    status = models.CharField(max_length=50, choices=CHOICE.choices, default=CHOICE.pending ,verbose_name='订单状态')

    class Meta:
        verbose_name = '订单'

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
