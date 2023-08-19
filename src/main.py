from src.gui import gui

from windows_toasts import Toast, WindowsToaster
toaster = WindowsToaster('Python')
newToast = Toast()


class Main:


def run(img, i, detector, data, dropdown):
    i += 1

    # Setup
    img = detector.find_pose(img)
    detector.get_position(img)  # DO NOT DELETE: this will give the landmark list

    # Interested angle
    # r_turn = detector.find_angle(img, 6, 8, 0)
    # l_turn = detector.find_angle(img, 3, 7, 0)
    front_posture = detector.find_angle(img, 11, 0, 12)
    left_shoulder = detector.find_angle(img, 9, 11, 12)
    right_shoulder = detector.find_angle(img, 10, 12, 11)

    good_poster = True

    # TODO: add an interator for good_posture so it only sends a notification if you slouch
    #  for a certain amount of time
    # TODO: right now the following measurements are for me. we need code to make it personalized
    if front_posture < data[dropdown]["front_p_min"] \
            or front_posture >  data[dropdown]["front_p_max"] \
            or left_shoulder <  data[dropdown]["left_s_min"] or left_shoulder >  data[dropdown]["left_s_max"] \
            or right_shoulder <  data[dropdown]["right_s_min"] or right_shoulder >  data[dropdown]["right_s_max"]:
        good_poster = False
    print(good_poster)

    if not good_poster and i > 100:
        newToast.text_fields = ['!']
        newToast.on_activated = lambda _: print('Toast clicked!')
        toaster.show_toast(newToast)
        i = 0
    return img


if __name__ == "__main__":
    Main()
