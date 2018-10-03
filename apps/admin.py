from django.contrib import admin
from .models import *
from django.forms.models import model_to_dict

# Register your models here.


admin.site.register(boxDeviceTable)
admin.site.register(wdjDeviceTable)
admin.site.register(voltDeviceTable)
admin.site.register(H2DeviceTable)
admin.site.register(H2ODeviceTable)
admin.site.register(CH4DeviceTable)
admin.site.register(CO2DeviceTable)
admin.site.register(AIRDeviceTable)
admin.site.register(N2DeviceTable)
admin.site.register(ovenDeviceTable)
admin.site.register(ovenPlanTable)
admin.site.register(ovenPlanDetailTable)
admin.site.register(cellDeviceTable)
admin.site.register(cellPlanTable)
admin.site.register(cellPlanDetailTable)
admin.site.register(BigTestInfoTable)
admin.site.register(testInfoTable)
admin.site.register(cellTestRealDataTable)
admin.site.register(eventTable)
admin.site.register(cellTestHistoryDataTable)










