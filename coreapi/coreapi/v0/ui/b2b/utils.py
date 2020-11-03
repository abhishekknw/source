from .models import Requirement

def get_lead_status(impl_timeline,meating_timeline,prefered_patners,company):
	
	if company == prefered_patners:
		change_current_patner = "yes"
	else:
		change_current_patner = "no"
	
	if change_current_patner == "yes":
		if impl_timeline == "immediate" and prefered_patners is not None:
			return "Deep Lead"
		elif (impl_timeline == "immediate" and meating_timeline == "immediate" \
			and prefered_patners == None) or (impl_timeline is not "immediate" and  \
			meating_timeline == "immediate" and prefered_patners is not None):
			return "Hot Lead"
		elif impl_timeline == "immediate" and meating_timeline is not "immediate" \
			and prefered_patners == None:
			return "Warm Lead"
		else:
			return "Lead"
	else:
		return "Raw Lead"