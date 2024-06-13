import sys
import NightEnforcer
import NightManager


def main():
    # length of sys argv is either 1 if the user opens the exe or 5 if the task scheduler runs the exe
    if len(sys.argv) > 1:
        activationTime = sys.argv[1]
        warningTime = int(sys.argv[2])
        snoozeTime = int(sys.argv[3])
        difficulty = int(sys.argv[4])
        NightEnforcer.NightEnforcer(activationTime, warningTime, snoozeTime, difficulty)
    else:
        NightManager.NightManager()


if __name__ == "__main__":
    main()