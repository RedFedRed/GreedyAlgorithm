import tkinter as tk
from tkinter import messagebox

class Teacher:
    def __init__(self, name):
        self.name = name
        self.assigned_subjects = []
        self.subject_count = 0

    def can_teach(self):
        return self.subject_count < 6  # Each teacher can teach a maximum of 6 subjects

    def assign_subject(self, subject):
        self.assigned_subjects.append(subject)
        self.subject_count += 1

    def __str__(self):
        return f"{self.name}: {', '.join(self.assigned_subjects)}"


class Subject:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Classroom:
    def __init__(self, room_number):
        self.room_number = room_number
        self.schedule = {}  # Dictionary to hold scheduled subjects

    def is_available(self, time_slot):
        return time_slot not in self.schedule  # Check if the time slot is already booked

    def assign_subject(self, subject, time_slot, teacher):
        self.schedule[time_slot] = (subject, teacher)

    def __str__(self):
        schedule_str = [f"{time}: {subject} by {teacher}" for time, (subject, teacher) in self.schedule.items()]
        return f"Classroom {self.room_number} Schedule:\n" + "\n".join(schedule_str)


class TimeSlot:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


def greedy_schedule(teachers, subjects, classrooms, time_slots):
    schedule = {}
    
    for subject in subjects:
        assigned = False  # Flag to check if the subject has been assigned
        
        for time_slot in time_slots:
            for classroom in classrooms:
                # Sort teachers by the number of subjects they are currently assigned
                available_teachers = sorted(teachers, key=lambda t: t.subject_count)
                
                for teacher in available_teachers:
                    if teacher.can_teach() and classroom.is_available(str(time_slot)):
                        # Assign the subject to the classroom and time slot
                        classroom.assign_subject(subject.name, str(time_slot), teacher.name)
                        teacher.assign_subject(subject.name)
                        schedule[subject.name] = (classroom.room_number, str(time_slot), teacher.name)
                        assigned = True
                        break
                if assigned:
                    break  # Break out of the classroom loop if a subject was assigned
            if assigned:
                break  # Break out of the time slot loop if a subject was assigned
        
        if not assigned:
            print(f"No available teacher for subject: {subject.name}")

    return schedule


class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher-Subject Scheduler")

        self.teachers = []
        self.subjects = []
        self.classrooms = []
        self.time_slots = []

        self.create_widgets()

    def create_widgets(self):
        # Input for teachers
        tk.Label(self.root, text="Teacher Name:").grid(row=0, column=0)
        self.teacher_entry = tk.Entry(self.root)
        self.teacher_entry.grid(row=0, column=1)
        tk.Button(self.root, text="Add Teacher", command=self.add_teacher).grid(row=0, column=2)

        # Input for subjects
        tk.Label(self.root, text="Subject Name:").grid(row=1, column=0)
        self.subject_entry = tk.Entry(self.root)
        self.subject_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Add Subject", command=self.add_subject).grid(row=1, column=2)

        # Input for classrooms
        tk.Label(self.root, text="Classroom Number:").grid(row=2, column=0)
        self.classroom_entry = tk.Entry(self.root)
        self.classroom_entry.grid(row=2, column=1)
        tk.Button(self.root, text="Add Classroom", command=self.add_classroom).grid(row=2, column=2)

        # Input for time slots
        tk.Label(self.root, text="Time Slot (e.g., 8:00 AM - 9:30 AM):").grid(row=3, column=0)
        self.time_slot_entry = tk.Entry(self.root)
        self.time_slot_entry.grid(row=3, column=1)
        tk.Button(self.root, text="Add Time Slot", command=self.add_time_slot).grid(row=3, column=2)

        # Button to generate schedule
        tk.Button(self.root, text="Generate Schedule", command=self.generate_schedule).grid(row=4, columnspan=3)

        # Text area to display the schedule
        self.schedule_text = tk.Text(self.root, width=50, height=15)
        self.schedule_text.grid(row=5, columnspan=3)

    def add_teacher(self):
        teacher_name = self.teacher_entry.get()
        if teacher_name:
            self.teachers.append(Teacher(teacher_name))
            self.teacher_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added teacher: {teacher_name}")
        else:
            messagebox.showwarning("Input Error", "Please enter a teacher name.")

    def add_subject(self):
        subject_name = self.subject_entry.get()
        if subject_name:
            self.subjects.append(Subject(subject_name))  # Corrected variable name
            self.subject_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added subject: {subject_name}")
        else:
            messagebox.showwarning("Input Error", "Please enter a subject name.")

    def add_classroom(self):
        classroom_number = self.classroom_entry.get()
        if classroom_number:
            self.classrooms.append(Classroom(classroom_number))
            self.classroom_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added classroom: {classroom_number}")
        else:
            messagebox.showwarning("Input Error", "Please enter a classroom number.")

    def add_time_slot(self):
        time_slot_str = self.time_slot_entry.get()
        if time_slot_str:
            start_time, end_time = time_slot_str.split(" - ")
            self.time_slots.append(TimeSlot(start_time.strip(), end_time.strip()))
            self.time_slot_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added time slot: {time_slot_str}")
        else:
            messagebox.showwarning("Input Error", "Please enter a time slot.")

    def generate_schedule(self):
        schedule = greedy_schedule(self.teachers, self.subjects, self.classrooms, self.time_slots)
        self.schedule_text.delete(1.0, tk.END)  # Clear previous schedule
        self.schedule_text.insert(tk.END, "Final Schedule:\n")
        for subject, (room, time, teacher) in schedule.items():
            self.schedule_text.insert(tk.END, f"{subject} is taught in Room {room} from {time} by {teacher}\n")

        self.schedule_text.insert(tk.END, "\nClassroom Assignments:\n")
        for classroom in self.classrooms:
            self.schedule_text.insert(tk.END, str(classroom) + "\n")


def main():
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()