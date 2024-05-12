"""
here's the implementation of my average day modeled by using FSM
"""

import random

def prime(fn):
    """enebles sending input"""
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

class FSM:
    """FSM class"""
    def __init__(self) -> None:

        self._hunger = 0
        self._fatigue = 0

        self.init = self._create_init()
        self.SLEEP = self._create_sleep()
        self.PROCRASTINATE = self._create_procrastinate()
        self.WORK_OUT = self._create_workout()
        self.STUDY = self._create_study()
        self.EAT = self._create_eat()
        self.DIE = self._create_die()

        self.current_state = self.init

    @property
    def hunger(self) -> int:
        """hunger getter"""
        return self._hunger

    @hunger.setter
    def hunger(self, val) -> None:
        """hunger setter"""
        if val >= 0:
            self._hunger = val
        else:
            self.hunger = 0

    @property
    def fatigue(self) -> int:
        """fatigue getter"""
        return self._fatigue

    @fatigue.setter
    def fatigue(self, val) -> int:
        """fatigue setter"""
        if val >= 0:
            self._fatigue = val
        else:
            self.fatigue = 0


    def send(self, hour_event):
        """sends input to machine"""
        try:
            self.current_state.send(hour_event)
        except StopIteration:
            print("The end.")

    def is_alive(self):
        """checks wether terminal state was reached"""
        return self.current_state != self.DIE

    @prime
    def _create_sleep(self):
        """sleep state"""
        while True:
            hour_event = yield
            hour, event = hour_event

            self.fatigue -= 1
            self.hunger += 0.5

            if self.hunger > 30:
                self.current_state = self.DIE
                print("You accidentaly swallowed your tongue when dreamed about juicy stake.")
            elif event == "air_alarm":
                self.current_state = self.PROCRASTINATE
                print("ATTENTION! Air alarm! Everyone should go to the shelter.")
            elif hour < 6:
                self.current_state = self.SLEEP
                print("Zzzzzzzz...")
            elif self.fatigue == 0:
                self.current_state = self.STUDY
                print("Ah! What a nice morning for discrete maths...")
            elif hour == 8 and self.fatigue < 5:
                self.current_state = self.EAT
                print("Yummy-yummy LET'S GO TO TRAPEZNA!")
            elif hour == 8.5 and self.fatigue < 10:
                self.current_state = self.STUDY
                print("Wakey-wakey! It's time for studying.")
            elif self.fatigue < 5:
                self.current_state = self.PROCRASTINATE
                print("Each and every outcome is already determined in our miserable world... \
Is there any point in trying to change sth helplessly..")
            elif 12 < hour < 16.5:
                self.current_state = self.PROCRASTINATE
            else:
                self.current_state = self.SLEEP
                print("Zzzz...")

    @prime
    def _create_eat(self):
        """eat state"""
        while True:
            hour_event = yield
            hour, event = hour_event

            self.hunger -= 10

            if self.fatigue >= 30 and self.hunger >= 30:
                self.current_state = self.DIE
                print("You were too exhasted, so you chocked with a food...")
            elif self.hunger == 0:
                self.current_state = self.PROCRASTINATE
                print("You ate too much and now you need a rest")
            elif event == "air_alarm":
                self.current_state = self.STUDY
                print("Luckily you ate in time and now you are ready to learn sth new.")
            elif hour == 8.5:
                self.current_state = self.STUDY
                print("What an awesome morning for studying!")
            elif self.fatigue < 3 and hour >= 10:
                self.current_state = self.WORK_OUT
                print("Let's pump a bicep quickly!")
            else:
                self.current_state = self.EAT
                print('"Sounds of consuming tasty food..."')

    @prime
    def _create_workout(self):
        """beast mode state"""
        while True:
            hour_event = yield
            hour, event = hour_event

            self.hunger += 5
            self.fatigue += 5

            if self.fatigue > 30:
                self.current_state = self.DIE
                print("The bar slipped from your hand, but you managed to caught it with your face...")
            elif hour < 6:
                self.current_state = self.SLEEP
                print("You've fallen sleep...")
            elif self.hunger >= 13:
                self.current_state = self.EAT
                print("Between dumbells and a barbell you've chosen to get a snack")
            elif self.fatigue <= 10 and hour <= 10:
                self.current_state = self.STUDY
                print("You cleared your mind for another portion of knowledge.")
            elif event == "meet_groupmate":
                self.current_state = self.STUDY
                print("You decided that it will be easier to study together with your mate.")
            elif self.fatigue in [19, 18]:
                self.current_state = self.PROCRASTINATE
                print("You're to tired for any activities except exloring latest social media posts.")
            else:
                self.current_state = self.WORK_OUT
                print("You are beaming with power and energy today!")

    @prime
    def _create_study(self):
        """nerd satate"""
        while True:
            hour_event = yield
            hour, event = hour_event

            self.fatigue += 2
            self.hunger += 2

            if self.fatigue > 25:
                self.current_state = self.SLEEP
                print("You were good today, get some rest...")
            
            elif event == "meet_groupmate":
                self.current_state = self.WORK_OUT
                print("Let's rock a local gym with your bruv")

            elif event == "random_motivation":
                self.current_state = self.STUDY
                print("Don't stop this guy... LET HIM STUDY!")
            elif hour < 6:
                self.current_state = self.SLEEP
                print("Dude... It's getting late. Take a nap")
            elif self.hunger > 15:
                self.current_state = self.EAT
                print("COOKIE! om nom nom")
            elif self.fatigue > 22:
                self.current_state = self.PROCRASTINATE
                print("I can't take it anymore...")

            else:
                self.current_state = self.STUDY
                print("I can be smarter, be better...[you are studying]")

    @prime
    def _create_procrastinate(self):
        """procrastinate state"""
        while True:
            hour_event = yield
            hour, event = hour_event

            self.hunger += 1
            self.fatigue += 1

            if event == "random_motivation" and hour < 6:
                self.current_state = self.WORK_OUT
                print("Never ever shall I procrastinate again! Allmightive PUUUUUSH![out of the blue you decided to work out]")
            elif hour in [8.5, 10, 15] and self.fatigue < 13:
                self.current_state = self.STUDY
                print("One way or another I ought to attend lessons...")
            elif event == "meet_groupmate":
                self.current_state = self.STUDY
                print("Your mate saved your efficiency rate...")
            elif self.fatigue < 3:
                self.current_state = self.WORK_OUT
                print("You gave yourself a chance for having better day and did some exercises.")
            elif self.hunger > 17 and hour < 22:
                self.current_state = self.EAT
                print("Your stomach managed to explain you the importance of eating on time")
            elif self.fatigue > 20:
                self.current_state = self.SLEEP
                print("Another pointless day...")
            else:
                self.current_state = self.PROCRASTINATE
                print("duh...[you are procrastinating]")

    @prime
    def _create_die(self):
        """terminal state"""
        while True:
            hour_event = yield
            print("The time has come for you...")
            break

    @prime
    def _create_init(self):
        """start state"""
        while True:
            hour_event = yield
            match random.choice([1,1,1,1,1,1,1,1,2,2,2,3,3]):
                case 1:
                    self.current_state = self.SLEEP
                    print("Zzzzz...")
                case 2:
                    self.current_state = self.STUDY
                    print("Deadlines kick hard...")
                case 3:
                    self.current_state = self.PROCRASTINATE
                    print("Duuuuuuuuh... procrastinating...")

def live_day(days=1, rarity=5):
    """main running function"""
    if days < 1 or rarity < 1:
        return None
    times = days * 48
    day = FSM()

    slept_hours = 0
    sport_done = 0
    inteligence_improved = 0
    procrastination_waste = 0

    for i in range(times):
        hour = (i/2)%24
        print(f">> {int(hour)}:{0 if not hour%1 else 3}0 <<", end = "   ")
        event = random.choice(["meet_groupmate", "air_alarm", "random_motivation"] + [None]*rarity)
        hour_event = (hour, event)
        day.send(hour_event)
        state = str(day.current_state)
        if "sleep" in state:
            slept_hours += 0.5
        elif "study" in state:
            inteligence_improved += 0.5
        elif "procrastinate" in state:
            procrastination_waste += 0.5
        elif "workout" in state:
            sport_done += 0.5
        if not day.is_alive():
            break

    print("You managed to live through another day" if day.is_alive() else \
"Even though you failed the mission, you were fighting with dignity.")
    print("="*20)
    print(f"""Your score:
Inteligence rate is {inteligence_improved} hours
Phisique rate is {sport_done} hours
Procrastination waste in hours is {procrastination_waste}""")
    print("="*20)
    if not day.is_alive():
        print("However, you died.")
        print("="*20)

if __name__ == "__main__":

    # change arguments here V
    live_day(14)
