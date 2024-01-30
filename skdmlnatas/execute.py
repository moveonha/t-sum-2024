from database import ChampionIndex
from train import DeepLearning
import numpy as np

ChampionIndex.make_chamdex_dict()
champions = ChampionIndex.champion_index

class Execution:
    def __init__(self):
        pass

    @staticmethod
    def run():
        sdp_champ = {}
        urp_champ = {}


        
        i = 0
        while len(sdp_champ)<5:
            tmp_sdp_champ = (input("상대 챔피언을 입력하세요: (취소하고 싶으면 해당 챔피언의 번호를 입력하세요)"))
            chg_champ = dict([(value, key) for (key, value) in sdp_champ.items()])
        
            if tmp_sdp_champ in chg_champ:
                print("이미 입력된 챔피언입니다.")
        
            elif tmp_sdp_champ in champions:
                i += 1
                sdp_champ[i] = tmp_sdp_champ
                print(sdp_champ)
        
            elif tmp_sdp_champ.isdigit():
                if 0 < int(tmp_sdp_champ) <6:
                    chg = (input("새로운 상대 챔피언을 입력하세요: "))
        
                    if chg in chg_champ:
                        print("이미 입력된 챔피언입니다.")
        
                    elif chg in champions:
                        sdp_champ[int(tmp_sdp_champ)] = chg
                        print(sdp_champ)
        
                    else:
                        print("존재하지 않는 챔피언 입니다. 다시 입력하세요.")
        
            else:
                print("존재하지 않는 챔피언 입니다. 다시 입력하세요.")
        
        answer = 1
        
        while answer != '':
        
            answer = input(f"{sdp_champ} 입력을 완료하시겠습니까?")
        
            if  answer.isdigit():
                if 0 < int(answer) <6:
                    chg = input("새로운 상대 챔피언을 입력하세요: ")
        
                    if chg in chg_champ:
                        print("이미 입력된 챔피언입니다.")
        
                    elif chg in champions:
                        sdp_champ[int(answer)] = chg
                        print(sdp_champ)
        
                    else:
                        print("존재하지 않는 챔피언 입니다. 다시 입력하세요.")



        i = 0
        while len(urp_champ)<4:
            tmp_sdp_champ = (input("아군 챔피언을 입력하세요: (취소하고 싶으면 해당 챔피언의 번호를 입력하세요)"))
            chg_champ = dict([(value, key) for (key, value) in urp_champ.items()])
        
            if tmp_sdp_champ in chg_champ:
                print("이미 입력된 챔피언입니다.")
        
            elif tmp_sdp_champ in champions:
                i += 1
                urp_champ[i] = tmp_sdp_champ
                print(urp_champ)
        
            elif tmp_sdp_champ.isdigit():
                if 0 < int(tmp_sdp_champ) <6:
                    chg = (input("새로운 아군 챔피언을 입력하세요: "))
        
                    if chg in chg_champ:
                        print("이미 입력된 챔피언입니다.")
        
                    elif chg in champions:
                        urp_champ[int(tmp_sdp_champ)] = chg
                        print(urp_champ)
        
                    else:
                        print("존재하지 않는 챔피언 입니다. 다시 입력하세요.")
        
            else:
                print("존재하지 않는 챔피언 입니다. 다시 입력하세요.")
        
        answer = 1
        
        while answer != '':
        
            answer = input(f"{urp_champ} 입력을 완료하시겠습니까?")
        
            if  answer.isdigit():
                if 0 < int(answer) <6:
                    chg = input("새로운 아군 챔피언을 입력하세요: ")
        
                    if chg in chg_champ:
                        print("이미 입력된 챔피언입니다.")
        
                    elif chg in champions:
                        urp_champ[int(answer)] = chg
                        print(urp_champ)
        
                    else:
                        print("존재하지 않는 챔피언 입니다. 다시 입력하세요.")

        user_data = [value for (key, value) in sdp_champ.items()]
        user_data += [value for (key, value) in urp_champ.items()]

        vd = {}
        for cmp in champions:

            tmp_user_data = user_data
            tmp_user_data.append(cmp)

            
            vd[cmp] = DeepLearning.exreal(tmp_user_data)

        vl = sorted(champions.items(), key=lambda x: x[1], reverse=True)
        for i in range(10):
            print(vl[i])