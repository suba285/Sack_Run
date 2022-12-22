
from screen_info import global_monitor_height, global_monitor_width

monitor_width = global_monitor_width
monitor_height = global_monitor_height

sheight = 270
swidth = 480

if monitor_width / 16 <= monitor_height / 9:
    fullscreen_scale = round(monitor_width / swidth)
    swidth = round(monitor_width / fullscreen_scale)
    sheight = round(swidth / 16 * 9)


def display_frames_per_second(screen, fps, num_list):
    string_fps = str(fps)
    number = list(string_fps)
    iteration = 0

    num0 = num_list[0]
    num1 = num_list[1]
    num2 = num_list[2]
    num3 = num_list[3]
    num4 = num_list[4]
    num5 = num_list[5]
    num6 = num_list[6]
    num7 = num_list[7]
    num8 = num_list[8]
    num9 = num_list[9]

    output1 = num0
    output2 = num0

    for digit in number:
        if digit == "0":
            image = num0
        elif digit == "1":
            image = num1
        elif digit == "2":
            image = num2
        elif digit == "3":
            image = num3
        elif digit == "4":
            image = num4
        elif digit == "5":
            image = num5
        elif digit == "6":
            image = num6
        elif digit == "7":
            image = num7
        elif digit == "8":
            image = num8
        elif digit == "9":
            image = num9
        else:
            image = num0

        if iteration == 0:
            output1 = image
        elif iteration == 1:
            output2 = image

        iteration += 1

    screen.blit(output1, (swidth - 20, sheight - 20))
    screen.blit(output2, (swidth - 15, sheight - 20))


