from .models import Requirement

def get_lead_status(impl_timeline,meating_timeline,prefered_patners,
	company,change_current_patner):
	
	prefered_patner = "no"
	if prefered_patners:
		prefered_patner = "yes"

	if change_current_patner == "yes":
		if impl_timeline == "within 2 weeks" and prefered_patner == "yes":
			return "Deep Lead"
		elif impl_timeline == "within 2 weeks" and meating_timeline == "as soon as possible" \
			and prefered_patner == "no":
			return "Hot Lead"
		elif (impl_timeline == "within 2 weeks" and meating_timeline is not "as soon as possible" \
			and prefered_patner == "no") or (impl_timeline is not "within 2 weeks" and  \
			meating_timeline == "as soon as possible" and prefered_patner == "yes"):
			return "Warm Lead"
		else:
			return "Lead"
	else:
		return "Raw Lead"
