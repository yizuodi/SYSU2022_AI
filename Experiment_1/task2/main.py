def print_result(player1_input, player2_input):
    if player1_input == player2_input:
        print('Ended in a draw!')
    elif (player1_input == "Rock" and player2_input == "Scissors") or (
            player1_input == "Scissors" and player2_input == "Paper") or (
            player1_input == "Paper" and player2_input == "Rock"):
        print('Congratulate Player1!')
    else:
        print('Congratulate Player2!')


def is_not_vaild(player_input):  # 如果输入非法，则返回true
    if player_input == "Rock":
        return False
    elif player_input == "Scissors":
        return False
    elif player_input == "Paper":
        return False
    return True


s = "y"
print('欢迎来到 两人石头剪刀布游戏 ')
while s == "y":
    s = ""
    player1_input = ""
    player2_input = ""
    while is_not_vaild(player1_input) or is_not_vaild(player2_input):
        if player1_input != "":
            print("您的输入有误!")
        print("请输入：Rock/Scissors/Paper")
        player1_input = input("Player1 input:")
        player2_input = input("Player2 input:")
    print_result(player1_input, player2_input)
    while s != "y" and s != "n":
        s = input("Try new game?(y/n)")
        if s != "y" and s != "n":
            print("您的输入有误！")
print("byebye!")