import numpy as np #
from sklearn.ensemble import RandomForestRegressor


class Task:
    def __init__(self, name, urgency, importance, effort):
        self.name = name
        self.urgency = urgency
        self.importance = importance
        self.effort = effort
        self.priority_score = self.calculate_priority()

    def calculate_priority(self):
        # Calculate priority based on urgency, importance, and effort as well as their weights
        return (self.urgency * 0.4 + self.importance * 0.4 + self.effort * 0.2)
        # The decimals represent how much of the total priority each other these categories make up for the priority

    def update_task(self, urgency=None, importance=None, effort=None): # 
        if urgency is not None:
            self.urgency = urgency
        if importance is not None:
            self.importance = importance
        if effort is not None:
            self.effort = effort
        self.priority_score = self.calculate_priority()

    # Showing the user an initilization of the code 
    def __repr__(self): #Overwriting the repr dunder function to get a display of the task and the categories the make up its priority
        return f"Task(name={self.name}, urgency={self.urgency}, importance={self.importance}, effort={self.effort}, priority={self.priority_score:.2f})"

# This class is created to handle prioritization of tasks through machine learning and provide recommendations based on the priority
#scores that the AI model has calculated
class AITaskPrioritization:
    def __init__(self, tasks): 
        self.tasks = tasks # tasks is a list of task objects that will be put together 
        self.model = RandomForestRegressor() 
        #RandomForestRegressor is a machine learning model from sklearn that was created for regression tasks such as predicting continuous variables
        #In the case of this project, it is being used to help predict the priority score of each task based on features like urgency, importance and effort
        #It uses decision trees which is a way to make a decision based on certain conditions. In this case, it is basedon the priority features.
        #This model creates multiple decision trees thus creating a forest that allows the models to try to average the predictions that are less likely to overfit the data
        self.train_model() # Calls the train_model method defined below

    def train_model(self): # This function is used to help train RandomForestRegressor 
        # Sample training data (features: urgency, importance, effort; labels: priority)
        features = np.array([[5, 8, 3], [9, 10, 2], [3, 4, 8], [7, 6, 5]]) 
        priority_labels = np.array([8.5, 9.2, 6.0, 7.5])
        self.model.fit(features, priority_labels) # Triggers the model to train based on the given data

    def update_task_priorities(self):
        # Update task priorities based on AI model predictions
        for task in self.tasks:
            predicted_priority = self.model.predict([[task.urgency, task.importance, task.effort]])[0] # Come back to this later.Model predicts the priority score of every task in the self.tasks list
            task.priority_score = predicted_priority

    def recommend_task(self):
        # AI recommends the task with the highest priority
        recommended_task = max(self.tasks, key=lambda x: x.priority_score) #Finding the max priority score for the task. Come back to this line because I need to understand the lambda expression.
        return recommended_task


class TaskManager:
    def __init__(self):
        self.tasks = [] #Creating a storage location for all the tasks and the details for every task

    def add_task(self, name, urgency, importance, effort):
        new_task = Task(name, urgency, importance, effort)
        self.tasks.append(new_task)

    def display_tasks(self):
        # Display all tasks with their priority scores
        if not self.tasks:
            print("No tasks available.")
        for task in self.tasks:
            print(task)

    def update_task(self, task_name, urgency=None, importance=None, effort=None):
        # Update the attributes of an existing task
        for task in self.tasks:
            if task.name == task_name:
                task.update_task(urgency, importance, effort)
                print(f"Task '{task_name}' updated.")
                break
        else:
            print(f"Task '{task_name}' not found.")


def interact_with_ai(task_manager, ai_system):
    while True:
        print("\nTask Prioritization System - AI Interaction")
        print("1. Add Task")
        print("2. Display Tasks")
        print("3. Update Task")
        print("4. Update Priorities with AI")
        print("5. Get AI Recommendation")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter task name: ")
            urgency = int(input("Enter urgency (1-10): "))
            importance = int(input("Enter importance (1-10): "))
            effort = int(input("Enter effort (1-10): "))
            task_manager.add_task(name, urgency, importance, effort)

        elif choice == "2":
            task_manager.display_tasks()

        elif choice == "3":
            task_name = input("Enter the task name to update: ")
            urgency = int(input("Enter new urgency (1-10): "))
            importance = int(input("Enter new importance (1-10): "))
            effort = int(input("Enter new effort (1-10): "))
            task_manager.update_task(task_name, urgency, importance, effort)

        elif choice == "4":
            ai_system.update_task_priorities()
            print("Task priorities updated based on AI predictions.")

        elif choice == "5":
            recommended_task = ai_system.recommend_task()
            print(f"AI recommends focusing on: {recommended_task.name} with priority {recommended_task.priority_score:.2f}")

        elif choice == "6":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


# Example usage
task_manager = TaskManager()
ai_system = AITaskPrioritization(task_manager.tasks)

# Start the interactive session
interact_with_ai(task_manager, ai_system)
