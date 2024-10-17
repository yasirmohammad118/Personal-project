import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root123",
    database="gym_management"
)
mycr = mydb.cursor()


# Function to log in
def id_pass():
    print("=== Gym Management System ===")
    print("Please log in to continue.")
    print("-x" * 20)
    
    # Loop until valid credentials are provided
    while True:
        u1 = input("Enter Username: ")
        p1 = input("Enter password: ")
        u2 = "Yasir"
        p2 = "7081"
        
        if u1 == u2 and p1 == p2:
            print("Welcome Admin")
            print("-x" * 20)
            menu()  # Show the menu after logging in
            break  # Exit the login loop on successful login
        else:
            print("Invalid username or password. Please try again.")
            print("-x" * 20)


# Function to display the menu
def menu():        
    while True:
        print("=== Main Menu ===")
        print("1. Show Existing Members")
        print("2. Add a New Member")
        print("3. Delete a Member")
        print("4. Search for a Member by Name")
        print("5. Exit")
        print("-x" * 20)
        
        ch1 = int(input("Enter your choice: "))
        
        print("-x" * 20)
        
        if ch1 == 1:
            exis()
        elif ch1 == 2:
            new_mem()
        elif ch1 == 3:
            dltmem()
        elif ch1 == 4:
            search_member_by_name()
        elif ch1 == 5:
            print("Exiting... Thank you for using the Gym Management System!")
            mydb.close()  # Close the database connection
            exit()
        else:
            print("Invalid choice. Please try again.")
            print("-x" * 20)


# Function to show existing members
def exis():
    print("=== Existing Members ===")
    mycr.execute("SELECT * FROM members")
    members = mycr.fetchall()  # Fetch all members
    if members:
        for i in members:
            print(f"Member ID: {i[3]}, Name: {i[0]}, Age: {i[1]}, Body Weight: {i[2]} kg")
    else:
        print("No members found.")
    print("-x" * 20)


# Function to add a new member
def new_mem():
    print("=== Add New Member ===")
    
    m1 = input("Enter your name: ")
    m2 = int(input("Enter your age: "))
    m3 = float(input("Enter your body weight (in kg): "))
    b = int(input("Enter your member ID given by your trainer: "))
    
    # Create the table if it doesn't exist
    mycr.execute("""CREATE TABLE IF NOT EXISTS members (
        Name VARCHAR(30),
        Age INT,
        B_weight DECIMAL(5,1),
        mem_no INT PRIMARY KEY)""")
    
    # Insert new member
    sql = "INSERT INTO members (Name, Age, B_weight, mem_no) VALUES (%s, %s, %s, %s)"
    values = (m1, m2, m3, b)
    mycr.execute(sql, values)
    mydb.commit()
    print("Member added successfully.")
    
    print("-x" * 20)

    # Call pricing function to handle fees and display workout plans
    pricing(m2)  # Pass age to pricing function


# Function to handle pricing
def pricing(age):
    print('How do you want to join the gym?')
    print('1. Annually')
    print('2. Half-yearly')
    print('3. Quarterly')
    print('4. Monthly')
    
    op = input('Enter your choice: ')
    fee1 = 0
    
    # Determine the fee based on the choice
    if op == '1':
        fee1 = 14000
    elif op == '2':
        fee1 = 9000
    elif op == '3':
        fee1 = 6000
    elif op == '4':
        fee1 = 2500
    else:
        print("Invalid choice, no fee selected.")

    print("Your fee is", fee1)


    # Extra services
    extra_services = { '1': 2000, '2': 2000, '3': 2000, '4': 2000 }
    fee2 = 0

    print('Would you like some extra services?')
    print('1. Spa')
    print('2. Sauna')
    print('3. Zumba classes')
    print('4. Boxing')
    
    op1 = input("Enter your choice: ")
    if op1 in extra_services:
        fee2 += extra_services[op1]
    else:
        print("No extra services added.")
    
    while True:
        op3 = input('Would you like to add more options? (y/n): ')
        if op3.lower() == 'y':
            op1 = input("Enter your choice: ")
            if op1 in extra_services:
                fee2 += extra_services[op1]
            else:
                print("Invalid choice, no additional fee added.")
        elif op3.lower() == 'n':
            break
        else:
            print("Please enter 'y' or 'n'.")

    total_fee = fee1 + fee2
    print("YOUR TOTAL FEE IS", total_fee)
    print("-x" * 20)

    # Ask user whether they want to bulk or cut and display plans accordingly
    show_workout_plans(age)


# Function to delete a member
def dltmem():
    print("=== Delete a Member ===")
    c = int(input("Enter your membership number: "))
    sql = "DELETE FROM members WHERE mem_no = %s"
    mycr.execute(sql, (c,))
    
    if mycr.rowcount > 0:
        mydb.commit()
        print("Member deleted successfully.")
    else:
        print("No member found with that membership number.")
    print("-x" * 20)

# Function to search for a member by name
def search_member_by_name():
    print("=== Search for a Member by Name ===")
    name = input("Enter the name of the member to search: ")
    sql = "SELECT * FROM members WHERE Name LIKE %s"
    mycr.execute(sql, ('%' + name + '%',))  # Use wildcards for partial matches
    results = mycr.fetchall()
    if results:
        for member in results:
            print(f"Member ID: {member[3]}, Name: {member[0]}, Age: {member[1]}, Body Weight: {member[2]} kg")
    else:
        print("No members found with that name.")
    print("-x" * 20)

# Function to show workout plans based on age and goal (bulking or cutting)
def show_workout_plans(age):
    print("=== Workout Plans Based on Your Goals ===")
    
    # Ask user for their goal
    goal = input("Would you like to bulk or cut? (Enter 'bulk' or 'cut'): ").strip().lower()
    
    if goal not in ['bulk', 'cut']:
        print("Invalid option. Please enter 'bulk' or 'cut'.")
        return  # Exit the function if the input is invalid
    
    if age < 19:
        if goal == 'cut':
            print("Cutting Workout Plan for Ages 12-18:\n", cutting_workout_plan_12_to_18())
        else:
            print("Bulking Workout Plan for Ages 12-18:\n", bulking_workout_plan_12_to_18())
    elif 19 <= age <= 45:
        if goal == 'cut':
            print("Cutting Workout Plan for Ages 19-45:\n", cutting_workout_plan_19_to_45())
        else:
            print("Bulking Workout Plan for Ages 19-45:\n", bulking_workout_plan_19_to_45())
    elif 45 < age <= 60:
        if goal == 'cut':
            print("Cutting Workout Plan for Ages 45-60:\n", cutting_workout_plan_45_to_60())
        else:
            print("Bulking Workout Plan for Ages 45-60:\n", bulking_workout_plan_45_to_60())
    else:
        if goal == 'cut':
            print("Cutting Workout Plan for Ages Above 60:\n", cutting_workout_plan_above_60())
        else:
            print("Bulking Workout Plan for Ages Above 60:\n", bulking_workout_plan_above_60())
    
    print("-x" * 20)

# Define the workout plan functions
def cutting_workout_plan_12_to_18():
    workout_plan = """
    Weekly Workout Split (Cutting):

    Day 1: Full Body Strength Training
    - Bodyweight Squats: 3 sets x 10-12 reps
    - Push-Ups: 3 sets x 8-10 reps
    - Dumbbell Bench Press: 3 sets x 8-10 reps
    - Dumbbell Rows: 3 sets x 8-10 reps
    - Plank: 3 sets x 30-60 seconds

    Day 2: Cardio
    - Running or Cycling: 30-45 minutes

    Day 3: Rest

    Day 4: Upper Body Strength
    - Dumbbell Shoulder Press: 3 sets x 8-10 reps
    - Pull-Ups or Lat Pulldowns: 3 sets x 6-8 reps
    - Tricep Dips: 3 sets x 8-10 reps
    - Bicep Curls: 3 sets x 10-12 reps

    Day 5: Cardio
    - HIIT (High-Intensity Interval Training): 20-30 minutes

    Day 6: Lower Body Strength
    - Lunges: 3 sets x 10-12 reps
    - Deadlifts: 3 sets x 8-10 reps
    - Leg Press: 3 sets x 10-12 reps
    - Calf Raises: 3 sets x 12-15 reps

    Day 7: Rest
    """
    return workout_plan

def bulking_workout_plan_12_to_18():
    workout_plan = """
    Weekly Workout Split (Bulking):

    Day 1: Upper Body Strength
    - Bench Press: 4 sets x 6-8 reps
    - Bent Over Rows: 4 sets x 6-8 reps
    - Shoulder Press: 4 sets x 6-8 reps
    - Pull-Ups: 3 sets x 6-8 reps
    - Bicep Curls: 3 sets x 8-10 reps

    Day 2: Lower Body Strength
    - Squats: 4 sets x 6-8 reps
    - Deadlifts: 4 sets x 6-8 reps
    - Lunges: 3 sets x 8-10 reps
    - Calf Raises: 3 sets x 10-12 reps

    Day 3: Rest

    Day 4: Full Body Strength
    - Clean and Press: 4 sets x 6-8 reps
    - Dips: 3 sets x 8-10 reps
    - Plank: 3 sets x 30-60 seconds

    Day 5: Cardio (Light)
    - Walking or Light Jogging: 20-30 minutes

    Day 6: Hypertrophy (Volume Training)
    - Super Set: Bench Press & Bent Over Rows: 3 sets x 10-12 reps each
    - Super Set: Dumbbell Flyes & Tricep Extensions: 3 sets x 10-12 reps each

    Day 7: Rest
    """
    return workout_plan

def cutting_workout_plan_19_to_45():
    workout_plan = """
    Weekly Workout Split (Cutting):

    Day 1: Upper Body Strength
    - Bench Press: 4 sets x 8-10 reps
    - Dumbbell Rows: 4 sets x 8-10 reps
    - Shoulder Press: 4 sets x 8-10 reps
    - Pull-Ups: 3 sets x 6-8 reps
    - Plank: 3 sets x 30-60 seconds

    Day 2: Cardio
    - HIIT: 20-30 minutes

    Day 3: Lower Body Strength
    - Squats: 4 sets x 8-10 reps
    - Deadlifts: 4 sets x 8-10 reps
    - Lunges: 3 sets x 10-12 reps
    - Calf Raises: 3 sets x 10-12 reps

    Day 4: Rest

    Day 5: Full Body Circuit
    - Kettlebell Swings: 3 sets x 10-12 reps
    - Push-Ups: 3 sets x 8-10 reps
    - Mountain Climbers: 3 sets x 30 seconds

    Day 6: Cardio
    - Steady-State Cardio: 30-45 minutes

    Day 7: Rest
    """
    return workout_plan

def bulking_workout_plan_19_to_45():
    workout_plan = """
    Weekly Workout Split (Bulking):

    Day 1: Chest and Triceps
    - Barbell Bench Press: 4 sets x 6-8 reps
    - Incline Dumbbell Press: 3 sets x 8-10 reps
    - Dips: 3 sets x 8-10 reps
    - Skull Crushers: 3 sets x 8-10 reps

    Day 2: Back and Biceps
    - Deadlifts: 4 sets x 6-8 reps
    - Pull-Ups: 3 sets x 6-8 reps
    - Bent Over Rows: 3 sets x 8-10 reps
    - Bicep Curls: 3 sets x 10-12 reps

    Day 3: Rest

    Day 4: Legs
    - Squats: 4 sets x 6-8 reps
    - Leg Press: 3 sets x 8-10 reps
    - Lunges: 3 sets x 10-12 reps
    - Calf Raises: 4 sets x 10-12 reps

    Day 5: Shoulders and Abs
    - Shoulder Press: 4 sets x 8-10 reps
    - Lateral Raises: 3 sets x 10-12 reps
    - Plank: 3 sets x 30-60 seconds
    - Russian Twists: 3 sets x 15 reps

    Day 6: Active Recovery
    - Light Cardio: 20-30 minutes

    Day 7: Rest
    """
    return workout_plan

def cutting_workout_plan_45_to_60():
    workout_plan = """
    Weekly Workout Split (Cutting):

    Day 1: Upper Body Strength
    - Push-Ups: 3 sets x 8-10 reps
    - Dumbbell Rows: 3 sets x 8-10 reps
    - Shoulder Press: 3 sets x 8-10 reps
    - Plank: 3 sets x 30-60 seconds

    Day 2: Cardio
    - Low-Impact Cardio: 30-45 minutes

    Day 3: Lower Body Strength
    - Bodyweight Squats: 3 sets x 10-12 reps
    - Lunges: 3 sets x 8-10 reps
    - Calf Raises: 3 sets x 12-15 reps

    Day 4: Rest

    Day 5: Full Body Circuit
    - Kettlebell Swings: 3 sets x 10-12 reps
    - Dumbbell Chest Press: 3 sets x 8-10 reps
    - Mountain Climbers: 3 sets x 30 seconds

    Day 6: Rest

    Day 7: Cardio
    - Walking: 30-45 minutes
    """
    return workout_plan

def bulking_workout_plan_45_to_60():
    workout_plan = """
    Weekly Workout Split (Bulking):

    Day 1: Full Body Strength
    - Deadlifts: 3 sets x 6-8 reps
    - Bench Press: 3 sets x 6-8 reps
    - Squats: 3 sets x 6-8 reps

    Day 2: Active Recovery
    - Light Cardio: 20-30 minutes

    Day 3: Upper Body Hypertrophy
    - Dumbbell Flyes: 3 sets x 8-10 reps
    - Bent Over Rows: 3 sets x 8-10 reps
    - Lateral Raises: 3 sets x 10-12 reps

    Day 4: Lower Body Hypertrophy
    - Leg Press: 3 sets x 8-10 reps
    - Lunges: 3 sets x 10-12 reps
    - Calf Raises: 3 sets x 12-15 reps

    Day 5: Rest

    Day 6: Cardio
    - Moderate-Intensity: 30-45 minutes

    Day 7: Flexibility and Mobility
    - Yoga or Stretching: 30-45 minutes
    """
    return workout_plan

def cutting_workout_plan_above_60():
    workout_plan = """
    Weekly Workout Split (Cutting):

    Day 1: Upper Body Strength
    - Push-Ups: 2 sets x 8-10 reps
    - Dumbbell Rows: 2 sets x 8-10 reps
    - Shoulder Press: 2 sets x 8-10 reps
    - Plank: 2 sets x 20-30 seconds

    Day 2: Cardio
    - Low-Impact Cardio: 20-30 minutes

    Day 3: Lower Body Strength
    - Bodyweight Squats: 2 sets x 8-10 reps
    - Lunges: 2 sets x 8-10 reps

    Day 4: Rest

    Day 5: Full Body Circuit (Low-Impact)
    - Kettlebell Swings: 2 sets x 10-12 reps
    - Seated Dumbbell Press: 2 sets x 8-10 reps

    Day 6: Rest

    Day 7: Walking
    - 20-30 minutes at a comfortable pace
    """
    return workout_plan

def bulking_workout_plan_above_60():
    workout_plan = """
    Weekly Workout Split (Bulking):

    Day 1: Upper Body
    - Dumbbell Bench Press: 2 sets x 6-8 reps
    - Bent Over Dumbbell Rows: 2 sets x 6-8 reps
    - Lateral Raises: 2 sets x 10-12 reps

    Day 2: Lower Body
    - Bodyweight Squats: 2 sets x 10-12 reps
    - Lunges: 2 sets x 10-12 reps

    Day 3: Active Recovery
    - Gentle Stretching or Yoga: 20-30 minutes

    Day 4: Upper Body
    - Push-Ups: 2 sets x 6-8 reps
    - Seated Dumbbell Press: 2 sets x 6-8 reps

    Day 5: Lower Body
    - Leg Press: 2 sets x 6-8 reps
    - Calf Raises: 2 sets x 10-12 reps

    Day 6: Rest

    Day 7: Walking
    - 20-30 minutes at a comfortable pace
    """
    return workout_plan
