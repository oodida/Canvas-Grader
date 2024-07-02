from bakery import assert_equal
from bakery_canvas import get_courses
from bakery_canvas import get_submissions
import matplotlib.pyplot as plt
from datetime import datetime
#import sys

#my_user_token = sys.argv[1]

def count_courses(user_token: str) -> int:
    """
        Args:
            user_token (str): name of user
        Return:
            num_courses (int): returns num of user's courses
    """
    courses = get_courses(user_token)
    num_courses=0
    for i in courses:
        num_courses+=1
    return num_courses

assert_equal(count_courses('annie'), 6)
assert_equal(count_courses('jeff'), 6)
assert_equal(count_courses('pierce'), 0)
assert_equal(count_courses('troy'), 1)

def find_cs1(user_token: str)->int:
    """
        Args:
            user_token: name of user
        Returns:
            i.id (int): id of the user's course that has "CISC1" in it
            0 (int): return if "CISC1" is not within i.id
    """
    courses = get_courses(user_token)
    for i in courses:
        if i.code == "CISC1":
            return i.id
    return 0

assert_equal(find_cs1('annie'), 100167)
assert_equal(find_cs1('jeff'), 100167)
assert_equal(find_cs1('pierce'), 0)
assert_equal(find_cs1('troy'), 0)

def find_course(user_token: str, course_id: int)->str:
    """
        Args:
            user_token: name of user
            course_id: course of id of user
        Returns:
            i.name + " " + str(i.id) (str): string representation of the full name of the course with the given id
            "no course found" (str): returns if no course_id match is found within user_token
   """
    courses = get_courses(user_token)
    for i in courses:
        if course_id == i.id:
            return i.name
    return "no course found"

assert_equal(find_course('annie',679554), "Intro to Math")
assert_equal(find_course('jeff',679554), "Intro to Math")
assert_equal(find_course('pierce',0), "no course found")
assert_equal(find_course('troy',394382), "History of Ice Cream")

def render_courses(user_token: str)->str:
    """
        Args:
            user_token (str): name of user
        Returns:
            render (str): returns str of rendered courses
     """
    courses = get_courses(user_token)
    render = ""
    for i in courses:
        render+=str(i.id)+":"+" "+i.code+"\n"
    return render
      
assert_equal(render_courses('annie'), "679554: MATH101\n386814: ENGL101\n4182: SPAN101\n394382: ICRM304\n100167: CISC1\n134088: PHED201\n")
assert_equal(render_courses('jeff'), "679554: MATH101\n386814: ENGL101\n4182: SPAN101\n394382: ICRM304\n100167: CISC1\n134088: PHED201\n")
assert_equal(render_courses('pierce'), "")
assert_equal(render_courses('troy'), "394382: ICRM304\n")

def total_points(user_token: str, course_id: int)->int:
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
        Returns:
            points(int): number of points possible in the course
    """
    points = 0
    submissions = get_submissions(user_token,course_id)
    for submission in submissions:
        points+=submission.assignment.points_possible
    return points

assert_equal(total_points('annie', 679554), 420)
assert_equal(total_points('annie', 386814), 700)
assert_equal(total_points('annie', 100167), 1060)
assert_equal(total_points('jeff', 679554), 420)
assert_equal(total_points('jeff', 386814), 700)
assert_equal(total_points('troy', 394382), 100)

def count_comments(user_token: str, course_id: int)->int:
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
        Returns:
            comments(int): total comments across the submissions for the course
    """ 
    submissions = get_submissions(user_token,course_id)
    comments=0
    for submission in submissions:
        for comment in submission.comments:
            comments+=1
    return comments

assert_equal(count_comments("annie",679554),14)
assert_equal(count_comments("jeff",679554),5)

def ratio_graded(user_token: str, course_id: int)->str:
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
        Returns:
            ratio(str): string ratio representation of # of assignments graded compared to # of total assignments in the course
    """ 
    submissions=get_submissions(user_token,course_id)
    graded=0
    total_assignments=0
    for submission in submissions:
        if submission.status == "graded":
            graded+=1
        total_assignments+=1
    ratio = str(graded) + "/" + str(total_assignments)  
    return ratio          

def average_score(user_token: str, course_id: int)->float:
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
        Returns:
            average(float): average, unweighted score of all of the assignments in the course
    """
    submissions=get_submissions(user_token,course_id)
    scores=0
    points=0
    for submission in submissions:
        scores+=submission.score
        if submission.status == "graded":
            points+=submission.assignment.points_possible
    average = scores/points
    return average

assert_equal(average_score('annie', 679554), 0.95)
assert_equal(average_score('annie', 386814), 0.97)
assert_equal(average_score('jeff', 386814), 0.7)

def average_weighted(user_token: str, course_id: int)->float:
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
        Returns:
            average(float): average, weighted score of all of the assignments in the course
    """
    submissions=get_submissions(user_token,course_id)
    scores=0
    points=0
    for submission in submissions:
        scores+=submission.score*submission.assignment.group.weight
        if submission.status == "graded":
            points+=submission.assignment.points_possible*submission.assignment.group.weight
    average = scores/points
    return average

assert_equal(average_weighted('annie', 679554), 0.9471153846153846)
assert_equal(average_weighted('annie', 386814), 0.97)
assert_equal(average_weighted('jeff', 386814), 0.7)

def average_group(user_token: str, course_id: int, group_name: str)->float:
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
            group_name(str): group name of assignment
        Returns:
            average(float): average, unweighted score of all of the assignments in the course
    """
    submissions=get_submissions(user_token,course_id)
    scores=0.0
    points=0.0
    for submission in submissions:
        if submission.assignment.group.name.lower() == group_name.lower():
            scores+=submission.score
            if submission.status == "graded":
                points+=submission.assignment.points_possible
    if points == 0.0:
        average = 0.0
    else:
        average = scores/points
    return average 

assert_equal(average_group('annie', 679554,"homework"), 0.9636363636363636)
assert_equal(average_group('annie', 386814,"homework"), 0.0)
assert_equal(average_group('jeff', 386814,"homework"), 0.0)

def render_assignment(user_token: str, course_id: int, assignment_id: int)->str:
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
            assignment_id(int): assignment's id from submission
        Returns:
            render(str): string representing the assignment and its submission details
    """
    submissions=get_submissions(user_token,course_id)
    render=""
    a_id=""
    group=""
    module=""
    grade=""
    a=0
    space=" "
    for submission in submissions:
        if submission.assignment.id == assignment_id:
            a=submission.assignment
            a_id=str(a.id)+":"+space+a.name
            group="Group:"+space+a.group.name
            module="Module:"+space+a.module
            if submission.status == "graded":
                grade="Grade:"+space+str(submission.score)+"/"+str(a.points_possible)+space+"("+submission.grade+")"
            else:
                grade="Grade:"+space+"(missing)"
            render=a_id+"\n"+group+"\n"+module+"\n"+grade
    if render:
        return render
    return "Assignment not found:"+space+str(assignment_id)
assert_equal(render_assignment('annie', 679554, 7), 'Assignment not found: 7')
assert_equal(render_assignment('annie', 679554, 299650), '299650: Introduction\nGroup: Homework\nModule: Module 1\nGrade: 10.0/10 (A)')
assert_equal(render_assignment('annie', 679554, 553716), '553716: Basic Addition\nGroup: Homework\nModule: Module 2\nGrade: 14.0/15 (A)')
assert_equal(render_assignment('annie', 679554, 805499), '805499: Basic Subtraction\nGroup: Homework\nModule: Module 2\nGrade: 19.0/20 (A)')
assert_equal(render_assignment('annie', 134088, 937202), '937202: Technology in the outdoor classroom\nGroup: Homework\nModule: Module 2\nGrade: (missing)')

def render_all(user_token: str, course_id: int)->str:
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
        Returns:
            render(str): single string that describes all of the submissions in the course
    """
    render=""
    submissions=get_submissions(user_token,course_id)
    for submission in submissions:
        a=submission.assignment
        a_id=str(a.id)+":"+" "+a.name
        if submission.status == "graded":
            render+=a_id+" "+"("+submission.status+")"+"\n"
        else:
            render+=a_id+" "+"("+"ungraded"+")"+"\n"
    return render

assert_equal(render_all('troy', 394382),"711675: Practical (graded)")
assert_equal(render_all('troy', 394382),"711675: Practical (graded)")

def plot_scores(user_token: str, course_id: int):
    """
        Args:
            user_token(str): user_token(str): user's canvas token
            course_id(int): user's chosen course id
        Returns:
            void
    """
    submissions = get_submissions(user_token, course_id)
    scores=[]
    score=0
    for i in submissions:
        if i.score != 0 and i.status == "graded":
            score=(i.score/i.assignment.points_possible)*100
            scores.append(score)
    plt.hist(scores)
    plt.title("Fractional Scores in the Course")
    plt.xlabel("courses")
    plt.ylabel("scores")
    plt.show()


plot_scores('annie', 100167)
plot_scores('abed', 100167)
plot_scores('jeff', 100167)

def days_apart(first_date: str, second_date: str) -> int:
    """
    Determines the days between `first` and `second` date.
    Do not modify this function!
    """
    first_date = datetime.strptime(first_date, "%Y-%m-%dT%H:%M:%S%z")
    second_date = datetime.strptime(second_date, "%Y-%m-%dT%H:%M:%S%z")
    difference = second_date - first_date
    return difference.days

def plot_earliness(user_token: str, course_id: int):
    """
        Args:
            user_token(str): user's canvas token
            course_id(int): user's chosen course_id
        Returns:
            void
    """
    submissions=get_submissions(user_token, course_id)
    difference=[]
    for i in submissions:
        if i.submitted_at and i.assignment.due_at:
            difference.append(days_apart(i.submitted_at,i.assignment.due_at))
    plt.hist(difference)
    plt.title("Distribution of Lateness")
    plt.xlabel("submissions")
    plt.ylabel("lateness")
    plt.show()

plot_earliness('annie', 100167)
plot_earliness('abed', 100167)
plot_earliness('jeff', 100167)

def plot_points(user_token: str, course_id: int):
    """
        Args:
            user_token(str): user_token(str): user's canvas token
            course_id(int): user's chosen course id
        Returns:
            void
    """
    submissions=get_submissions(user_token,course_id)
    points_possible=[]
    total_weighted=0
    weighted_possible=[]
    weight=0
    points=0
    for a in submissions:
        total_weighted+=a.assignment.points_possible*a.assignment.group.weight
    total_weighted/=100
    if total_weighted != 0:
        for b in submissions:
            points = b.assignment.points_possible
            weight=b.assignment.group.weight
            points_possible.append(points)
            weighted_possible.append((points*weight)/total_weighted)
    plt.scatter(points_possible,weighted_possible)
    plt.title("Points Possible")
    plt.xlabel("submissions")
    plt.ylabel("comparisons")
    plt.show()
    
plot_points('annie', 100167)
plot_points('annie', 679554)
plot_points('annie', 386814)

def predict_grades(user_token: str, course_id: int):
    """
        Args:
            user_token(str): user_token(str): user's canvas token
            course_id(int): user's chosen course id
        Returns:
            void
    """
    submissions=get_submissions(user_token,course_id)
    total_weighted=0
    for a in submissions:
        total_weighted+=a.assignment.points_possible*a.assignment.group.weight
    total_weighted/=100
    #total weighted points
    max_points=[]
    max_scores=[]
    min_scores=[]
    
    max_point=0
    max_score=0
    min_score=0
   
    for b in submissions:
        points=b.assignment.points_possible
        weight=b.assignment.group.weight
        score=b.score
        if b.status == "graded":
            max_point+=(points*weight)/total_weighted
            max_score+=(score*weight)/total_weighted
            min_score+=(score*weight)/total_weighted
            
            max_points.append(max_point)
            max_scores.append(max_score)
            min_scores.append(min_score)
        else:
            max_point+=(points*weight)/total_weighted
            max_score+=(points*weight)/total_weighted
            min_score+=(0*weight)/total_weighted
            
            max_points.append(max_point)
            max_scores.append(max_score)
            min_scores.append(min_score)
    plt.plot(max_points)
    plt.plot(max_scores)
    plt.plot(min_scores)
    plt.ylim([0,100])
    plt.title("Grade Prediction")
    plt.xlabel("assignments")
    plt.ylabel("course grades")
    plt.show()
        

print("Introduction to Computer Science")
predict_grades('annie', 100167)
predict_grades('abed', 100167)
predict_grades('jeff', 100167)
print("Physical Education Education")
predict_grades('annie', 134088)
predict_grades('abed', 134088)
predict_grades('jeff', 134088)


def execute(command: str, user_token: str, course_id: int)->int:
    """
        Args:
            command (str): command that the user inputs
            user_token (str): token of the user
            course_id (int): specific course id from the user_token 
        Returns:
            new_course.id(int): returns new course
            course_id(int): returns id of specific course
    """
    user_input = ""
    if command == "course":
        print(render_courses(user_token)) 
        user_input = int(input("What is the id of the new course?"))
        new_course = find_course(user_token, user_input)
        print(new_course)
        return user_input
    elif command == "exit":
        return 0
    elif command == "points":
        print(total_points(user_token,course_id))
    elif command == "comments":
        print(count_comments(user_token,course_id))
    elif command == "graded":
        print(ratio_graded(user_token,course_id))
    elif command == "score_unweighted":
        print(average_score(user_token,course_id))
    elif command == "score":
        print(average_weighted(user_token,course_id))
    elif command == "group":
        user_input = input("What is the group name?")
        print(average_group(user_token,course_id,user_input))
    elif command == "assignment":
        user_input = int(input("What is the assignment ID?"))
        print(render_assignment(user_token,course_id,user_input))
    elif command == "list":
        print(render_all(user_token,course_id))
    elif command == "scores":
        print(plot_scores(user_token,course_id))
    elif command == "earliness":
        print(plot_earliness(user_token,course_id))
    elif command == "compare":
        print(plot_points(user_token,course_id))
    elif command == "predict":
        print(predict_grades(user_token,course_id))
    elif command == "help":
        print("""exit > Exit the application
\n help > List all the commands
\n course > Change current course
\n points > Print total points in course
\n comments > Print how many comments in course
\n graded > Print ratio of ungraded/graded assignments
\n score_unweighted > Print average unweighted score
\n score > Print average weighted score
\n group > Print average of assignment group, by name
\n assignment > Print the details of a specific assignment, by ID
\n list > List all the assignments in the course
\n scores > Plot the distribution of grades in the course
\n earliness > Plot the distribution of the days assignments were submitted early
\n compare > Plot the relationship between assignments' points possible and their weighted points possible
\n predict > Plot the trends in grades over assignments, showing max ever possible, max still possible, and minimum still possible """)
    return course_id

def main(user_token: str):
    """
        Args:
            user_token: token of the user
        Returns:
            void
    """
    courses = get_courses(user_token)
    default = 0 
    user_input2 = ""
    if count_courses(user_token):
        default = find_cs1(user_token) 
        if not default: 
            default = courses[0].id 
        while default > 0: 
            user_input2 = input("What would you like to do? Course, help, or exit?")
            default = execute(user_input2, user_token, default)
    return "no courses available"