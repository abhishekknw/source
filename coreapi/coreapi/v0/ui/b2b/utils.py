from .models import Requirement

def get_lead_status(impl_timeline,meating_timeline,prefered_patners,
	company,change_current_patner):
	
	prefered_patner = "no"
	for row in prefered_patners:
		if company == row:
			prefered_patner = "yes"

	if change_current_patner == "yes":
		if impl_timeline == "immediate" and prefered_patners == "yes":
			return "Deep Lead"
		elif (impl_timeline == "immediate" and meating_timeline == "immediate" \
			and prefered_patners == "no") or (impl_timeline is not "immediate" and  \
			meating_timeline == "immediate" and prefered_patners == "yes"):
			return "Hot Lead"
		elif impl_timeline == "immediate" and meating_timeline is not "immediate" \
			and prefered_patners == "no":
			return "Warm Lead"
		else:
			return "Lead"
	else:
		return "Raw Lead"