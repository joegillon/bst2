from models.voter import Voter
from models.neighborhood import Neighborhood


nhood = Neighborhood.get_one('Ann Arbor', 'Garden Homes')
Voter.build_my_voters(nhood)
