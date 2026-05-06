from accounts.models import Profile
from commissions.models import Commission, CommissionType
from commissions.services import CommissionService

# 1. Setup a valid profile and type
maker = Profile.objects.first()
c_type = CommissionType.objects.get_or_create(name="Test Type")[0]

# 2. INTENTIONALLY BAD DATA: Provide a negative manpower number
# (Assuming your model has a check or you force an error here)
bad_jobs_data = [{'role': 'Dev', 'manpower_required': -100}]
valid_comm_data = {'title': 'Should Not Exist', 'description': '...', 'type': c_type, 'people_required': 1}

try:
    CommissionService.create_commission(maker, valid_comm_data, bad_jobs_data)
except Exception as e:
    print(f"Caught expected error: {e}")

# 3. VERIFY: The commission should NOT be in the database
exists = Commission.objects.filter(title='Should Not Exist').exists()
print(f"Was the commission saved despite the error? {exists} (Should be False)")