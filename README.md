# Wellesley Computational Housing Economics Lab (CHEL)
# Policy-Oriented Mortgage Simulator
- Currently implements the Wellesley Faculty Mortgage Program, an interest-only program for the second loan. It can be adjusted to other programs through user input of parameters

For local deployement during development:
1. Install streamlit if needed: ```pip install streamlit```
2. Run ```streamlit run scripts/app.py``` to see application in your browser (should pop up automatically)

To see the current website:
https://wellesleychel.streamlit.app

# About The Repository
Code
- All code files are under the ```scripts``` folder
- Edit ```app.py``` for anything that displays on the front-end
- There are separate files for the graph helper functions: ```bar_graph.py``` creates the first stacked bar graph for with and without the program, and ```equality_line_graph.py``` creates the second graph showing the AMI (annual median income) boxes with the 45 degrees line. Add more modular files like this for any new graphs.
- ```utils.py``` contains all other reusable code. It includes constants like ```DATA_FILE_PATH``` for the main excel sheet, and ```TOWNS``` for the list of all MA towns for easy reuse. There's also WELLESLEY_MAX_SECOND_LOAN and WELLESLEY_AFR_FRACTION which are the default for the Wellesley faculty program. To use these constants in another file, simply do ```from utils import [constant]```, e.g. ```from utils import TOWNS```. Keep constants capitalized.

Data
- Data files go under the  ```data``` folder. Currently it only contains MortgageRatesData.xlsx, which is used by all graphs.

Requirements
- For streamlit to properly deploy with the necessary packages/libraries installed, rememeber to do ```pip freeze > requirements.txt```, or ```pip3 freeze > requirements.txt``` (if you are using Python3) so that streamlit can have your locally installed/imported packages available when hosting the application.

# Suggestions for Next Steps
1. Fix the legend on hover for the bar graph. Either remove the "difference" display, or fix the color coding.
2. Add year on the legend of the equality line graph, make it clickable so that the user can click on a year of interest and it highlights the corresponding dot on the graph.
3. Based on the equality line graph, add a tabular display of which towns, under the program, are unaffordable --> affordable, unaffordable --> unaffordable, affordable --> affordable, etc. for easier interpretation. This was shown at the lab meetings, so the code should be readily available (may just need to translate into Python)
4. Incorporate school ratings for unaffordable and affordable towns, with a slider showing the progression of it over time. This was also shown at the lab meetings.

For other policies
- If the policy is also interest-only and structured similar to the Wellesley Faculty Program, then you can simply input the new rates as the arguments to ```calculate_monthly_payments()``` like ```max_second_loan```, which are currently set with a default but also changes based on user input. Currently ```calculate_monthly_payments()``` resides in ```bar_graph.py```, but consider moving it to utils so that it is clear that it's shared among graphs (currently just imported from ```bar_graph.py```).
- If the policy is of a different structure, either create a new ```calculate_monthly_payments()``` function, or add an additional argument to the current one that indicates which policy.
- To create separate pages for different policies, simply look at streamlit's built in function: see https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app.
