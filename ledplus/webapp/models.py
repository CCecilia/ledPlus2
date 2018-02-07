from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
import uuid


class RetailEnergyProvider(models.Model):
    name = models.CharField(max_length=254, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='rep_logos/')
    teams = models.ManyToManyField('Team', blank=True)
    rate_upload = models.FileField(upload_to='rates/')

    def __str__(self):
        return self.name
 

class Team(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)

    def __str__(self):
        return self.name


class Agent(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	retail_energy_provider = models.ForeignKey('RetailEnergyProvider', on_delete=models.CASCADE, blank=False, null=False)
	team = models.ForeignKey('Team', on_delete=models.PROTECT, blank=False, null=False)

	def __str__(self):
		return self.user.username


class Subtype(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False, unique=True)
    sunday = models.IntegerField(default=0)
    monday = models.IntegerField(default=0)
    tuesday = models.IntegerField(default=0)
    wednesday = models.IntegerField(default=0)
    thursday = models.IntegerField(default=0)
    friday = models.IntegerField(default=0)
    saturday = models.IntegerField(default=0)
    total_hours_of_operation = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Led(models.Model):
	COLORS = (
		('5000K', '5000K'),
		('2700K', '2700K')
	)
	LED_TYPE = (
		('Tube', 'Tube'),
		('U-BEND Tube', 'U-BEND Tube'),
		('Lamp', 'Lamp'),
		('Candelabra', 'Candelabra'),
		('Spot', 'Spot'),
		('Flood', 'Flood'),
		('Track', 'Track'),
		('4 pin', '4 pin'),
		('Fixture', 'Fixture'),
	)
	BALLASTS = (
		('Electronic', 'Electronic'),
		('Magnetic', 'Magnetic')
	)
	BRANDS = (
		('Philips', 'Philips'),
		('Forest', 'Forest'),
		('ELB', 'ELB'),
		('Satco', 'Satco'),
		('Sylvania', 'Sylvania'),
		('n/a', 'n/a'),
		('Way to Go', 'Way to Go'),
		('Green Creative', 'Green Creative'),
		('LED Plus', 'LED Plus')
	)

	name = models.CharField(max_length=254, blank=False, null=False)
	type = models.CharField(max_length=20, choices=LED_TYPE, default='Tube')
	ballast = models.CharField(max_length=20, choices=BALLASTS, default='Electronic')
	net_cost = models.DecimalField(max_digits=6, decimal_places=2)
	sale_price = models.DecimalField(max_digits=6, decimal_places=2)
	non_led_price = models.DecimalField(max_digits=6, decimal_places=2)
	image = models.ImageField(upload_to='led_images/')
	wattage = models.IntegerField(default=0)
	conventional_wattage = models.IntegerField(default=0)
	order_number = models.IntegerField(default=0)
	active = models.BooleanField(default=False)
	zero_to_fifty = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	fifty_one_to_two_hundred = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	two_hundred_one_to_five_hundred = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	five_hundred_to_one_thousand = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	min_visit_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	premium_ceiling_multiplier = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	brands = MultiSelectField(choices=BRANDS, default='Philips')
	colors = MultiSelectField(choices=COLORS, default='5000K')
	lumens = models.CharField(max_length=254, blank=True, null=True)
	rated_average_life = models.CharField(max_length=254, blank=True, null=True)

	def __str__(self):
		return str(self.name)


class SaleLed(models.Model):
	CEILING_HEIGHTS = (
		(1, 'Over 16`'),
		(2, '12` to 16`'),
		(3, 'Up to 12`')
	)
	led = models.ForeignKey('Led', on_delete=models.PROTECT)
	color = models.CharField(max_length=254, blank=False, null=False)
	led_count = models.IntegerField(default=0)
	total_count = models.IntegerField(default=0)
	not_replacing_count = models.IntegerField(default=0)
	delamping_count = models.IntegerField(default=0)
	wattage_reduction = models.DecimalField(max_digits=16, decimal_places=8, default=0)
	installation_required = models.BooleanField(default=True)
	ceiling_height = models.IntegerField(choices=CEILING_HEIGHTS, default=2)
	recycling = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)


class Sale(models.Model):
	BILL_TYPE = (
		('monthly', 'monthly'),
		('yearly', 'yearly')
	)
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Unique Identifier')
	agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False, null=False)
	date_created = models.DateTimeField(auto_now_add=True)
	renewal = models.BooleanField(default=False)
	business_name = models.CharField(max_length=100, blank=True, null=True)
	authorized_representative = models.CharField(max_length=100, blank=True, null=True)
	service_address = models.CharField(max_length=255, blank=True, null=True)
	service_city = models.CharField(max_length=255, blank=True, null=True)
	service_state = models.CharField(max_length=2, blank=True, null=True)
	service_zip_code = models.CharField(max_length=10, blank=True, null=True)
	subtype = models.ForeignKey(Subtype, on_delete=models.PROTECT, null=True)
	annual_hours_of_operation = models.IntegerField(default=0)
	leds = models.ManyToManyField('SaleLed')
	billing_address = models.CharField(max_length=255, blank=True, null=True)
	billing_city = models.CharField(max_length=255, blank=True, null=True)
	billing_state = models.CharField(max_length=2, blank=True, null=True)
	billing_zip_code = models.CharField(max_length=10, blank=True, null=True)
	utility = models.ForeignKey('Utility', on_delete=models.PROTECT, null=True)
	zone = models.ForeignKey('Zone', on_delete=models.PROTECT, null=True)
	service_class = models.ForeignKey('ServiceClass', on_delete=models.PROTECT, null=True)
	utility_account_number = models.CharField(max_length=255, blank=True, null=True, unique=True)
	bill_type = models.CharField(max_length=7, choices=BILL_TYPE, default='monthly')
	month_of_bill = models.CharField(max_length=2, blank=True, null=True)
	service_start_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
	bill_image = models.ImageField(upload_to='bill_images/', blank=True)
	kwh = models.IntegerField(default=0, verbose_name='kWh')
	supply_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	delivery_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	supply_rate = models.DecimalField(max_digits=6, decimal_places=5, default=0.0000)
	base_rate = models.DecimalField(max_digits=6, decimal_places=5, default=0.0000)
	logistics_adder = models.DecimalField(max_digits=6, decimal_places=5, default=0.0000)
	marketing_adder = models.DecimalField(max_digits=6, decimal_places=5, default=0.0000)
	energy_only_adder = models.DecimalField(max_digits=6, decimal_places=5, default=0)
	sales_tax = models.DecimalField(max_digits=6, decimal_places=5, default=0.0000)
	max_adder = models.DecimalField(max_digits=3, decimal_places=2, default=0.05)
	total_installation_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	# weight = models.DecimalField(max_digits=6, decimal_places=5, default=None)
    # customer_phone_number = models.CharField(max_length=255,blank=True,null=True)
    # customer_email_address = models.CharField(max_length=255,blank=True,null=True)
    # times_bulbs_changed_yearly = models.CharField(max_length=255,blank=True,null=True)
    # annual_hours_of_operation = models.CharField(max_length=255,blank=True,null=True)
    # service_class = models.CharField(max_length=255,blank=True,null=True)
    # yearly_kwh = models.CharField(max_length=255,blank=True,null=True)
    # monthly_kwh = models.CharField(max_length=255,blank=True,null=True)
    # supply_charges = models.CharField(max_length=255,blank=True,null=True)
    # delivery_charges = models.CharField(max_length=255,blank=True,null=True)
    # average_rate_of_supply = models.CharField(max_length=255,blank=True,null=True)
    # average_rate_of_delivery = models.CharField(max_length=255,blank=True,null=True)
    # estimated_annual_usage = models.CharField(max_length=255,blank=True,null=True)
    # estimated_annual_supply_charges = models.CharField(max_length=255,blank=True,null=True)
    # estimated_annual_delivery_charges = models.CharField(max_length=255,blank=True,null=True)
    # conventional_bulb_count = models.CharField(max_length=255,blank=True,null=True)
    # led_bulb_count = models.CharField(max_length=255,blank=True,null=True)
    # delamping_count = models.CharField(max_length=255,blank=True,null=True)
    # not_replacing_count = models.CharField(max_length=255,blank=True,null=True)
    # annual_bulb_maintenance = models.CharField(max_length=255,blank=True,null=True)
    # annual_consumption_reduction = models.CharField(max_length=255,blank=True,null=True)
    # projected_annual_usage = models.CharField(max_length=255,blank=True,null=True)
    # new_supply_rate = models.CharField(max_length=255,blank=True,null=True)
    # two_year_supply_savings = models.CharField(max_length=255,blank=True,null=True)
    # two_year_delivery_savings = models.CharField(max_length=255,blank=True,null=True)
    # two_year_maintenace_savings = models.CharField(max_length=255,blank=True,null=True)
    # total_two_year_savings = models.CharField(max_length=255,blank=True,null=True)
    # early_termination_fee = models.CharField(max_length=255,blank=True,null=True)
    # retail_energy_provider = models.CharField(max_length=255,blank=True,null=True)
    # agent_id = models.CharField(max_length=255,blank=True,null=True)
    # agent_name = models.CharField(max_length=255,blank=True,null=True)
    # old_sale_id = models.CharField(max_length=255,blank=True,null=True)
    # date_sale_started = models.CharField(max_length=255,blank=True,null=True)
    # date_sale_completed = models.CharField(max_length=255,blank=True,null=True)
    # customer_interest_level = models.CharField(max_length=255,blank=True,null=True)
    # customer_sub_type = models.CharField(max_length=255,blank=True,null=True)
    # weight = models.CharField(max_length=255,blank=True,null=True)
    # min_monthly_payment = models.CharField(max_length=255,blank=True,null=True)
    # led_adder = models.CharField(max_length=255,blank=True,null=True)
    # marketing_adder = models.CharField(max_length=255,blank=True,null=True)
    # logistics_adder = models.CharField(max_length=255,blank=True,null=True)
    # ee_adder = models.CharField(max_length=255,blank=True,null=True)
    # base_rate = models.CharField(max_length=255,blank=True,null=True)
    # tax_rate = models.CharField(max_length=255,blank=True,null=True)
    # customer_zone = models.CharField(max_length=255,blank=True,null=True)
    # ceiling_height = models.CharField(max_length=255,blank=True,null=True)
    # total_installation_cost = models.CharField(max_length=255,blank=True,null=True)
    # installation_adder = models.CharField(max_length=255,blank=True,null=True)
    # sales_team = models.CharField(max_length=255,blank=True,null=True)
    # parent_company = models.CharField(max_length=255,blank=True,null=True)
    # share_link = models.CharField(max_length=255,blank=True,null=True)
    # enrolled_status = models.BooleanField(default=False)
    # enrolled_date = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    # cancelled_date = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    # projected_flow_date = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    # REP_customer_account_number = models.CharField(max_length=255,blank=True,null=True)
    # shipped_status = models.CharField(max_length=255,blank=True,null=True)
    # ship_date = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    # installation_status = models.CharField(max_length=255,blank=True,null=True)
    # installation_date = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    # installation_company = models.CharField(max_length=255,blank=True,null=True)
    # cancellation_date = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    # notes = models.ManyToManyField('SaleNote',blank=True)
    # total_led_cost = models.CharField(max_length=255,blank=True,null=True)
    # total_led_price = models.CharField(max_length=255,blank=True,null=True)
    # REP_profit = models.CharField(max_length=255,blank=True,null=True)
    # total_green_bonus = models.CharField(max_length=254,blank=True,null=True)
    # brand = models.CharField(max_length=254,blank=True,null=True)
    # docusign_status = models.CharField(max_length=254,blank=True,null=True)
    # sale_type = models.CharField(max_length=254,blank=True,null=True)
    # cancelled = models.BooleanField(default=False)
    # renewal = models.BooleanField(default=False)
    # tracking_number = models.CharField(max_length=254,blank=True,null=True)
    # shipping_method = models.CharField(max_length=254,blank=True,null=True) 
    # bill_of_ladings = models.ManyToManyField('ImageUpload',blank=True) 
    # service_start_date = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    # broker_margin = models.CharField(max_length=254,blank=True,null=True)
    # rep_margin = models.CharField(max_length=254,blank=True,null=True)
    # ledplus_adder = models.CharField(max_length=254,blank=True,null=True)
    # energy_only_sale = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.business_name


class Zone(models.Model):
	zip_code = models.CharField(max_length=5, blank=False, null=False)
	name = models.CharField(max_length=254, blank=False, null=False)

	def __str__(self):
		return str(self.name)


class Utility(models.Model):
	name = models.CharField(max_length=254, blank=False, null=False)
	state = models.CharField(max_length=2, blank=False, null=False)
	account_digits = models.IntegerField(default=12)
	active = models.BooleanField(default=True)
	zone_lookup = models.BooleanField(default=False)
	zones = models.ManyToManyField('Zone', blank=True)

	def __str__(self):
		return str(self.name)


class ServiceClass(models.Model):
	name = models.CharField(max_length=254, blank=False, null=False)
	active = models.BooleanField(default=False)

	def __str__(self):
		return str(self.name)

