from graph import Graph
from inference import Inference
import copy

if __name__ == "__main__":
    
    #Alarm problem
    reportVariables = ['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT']
    littleEvidence = {'HRBP' : 'HIGH', 'CO' : 'LOW','BP' :'HIGH'}
    moderateEvidence = {'HRBP' : 'HIGH', 'CO' : 'LOW','BP' :'HIGH','HRSAT' : 'LOW','HREKG' : 'LOW','HISTORY' : 'TRUE'}

    initAlarmGraph = Graph("alarm.bif")
    alarmGraph = copy.deepcopy(initAlarmGraph)
    evidence = list()


    # print(initAlarmGraph)
    # alarmGraph = copy.deepcopy(initAlarmGraph)
    # print("P (HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT | None)")
    # alarmGraph.getApproximateProbability("HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT | None", 6000)

    print("P (HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT | None)")
    alarmGraph.getApproximateProbability("HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT | None", 10000)


    alarmGraph = copy.deepcopy(initAlarmGraph)
    print("P (HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT |  HRBP=HIGH; CO=LOW; BP=HIGH)")
    alarmGraph.getApproximateProbability("HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT |  HRBP=HIGH; CO=LOW; BP=HIGH", 10000)

    alarmGraph = copy.deepcopy(initAlarmGraph)
    print("P (HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT | HRBP=HIGH; CO=LOW; BP=HIGH; HRSAT=LOW; HREKG=LOW; HISTORY=TRUE)")
    alarmGraph.getApproximateProbability("HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT | HRBP=HIGH; CO=LOW; BP=HIGH; HRSAT=LOW; HREKG=LOW; HISTORY=TRUE", 10000)

    # Child Network
    initChildGraph = Graph("child.bif")

    childGraph = copy.deepcopy(initChildGraph)
    print("P (Disease | None)")
    childGraph.getApproximateProbability("Disease | None", 16000)

    childGraph = copy.deepcopy(initChildGraph)
    print("P (Disease | LowerBodyO2=“<5”; RUQO2=“>=12”; CO2Report=“>=7.5”; XrayReport=Asy/Patchy)")
    childGraph.getApproximateProbability("Disease | LowerBodyO2=“<5”; RUQO2=“>=12”; CO2Report=“>=7.5”; XrayReport=Asy/Patchy", 16000)

    childGraph = copy.deepcopy(initChildGraph)
    print("P (Disease | LowerBodyO2=“<5”; RUQO2=“>=12”; CO2Report=“>=7.5”; XrayReport=Asy/Patchy; GruntingReport=Yes; LVHReport=Yes; Age=“11-30 Days”)")
    childGraph.getApproximateProbability("Disease | LowerBodyO2=“<5”; RUQO2=“>=12”; CO2Report=“>=7.5”; XrayReport=Asy/Patchy; GruntingReport=Yes; LVHReport=Yes; Age=“11-30 Days”", 16000)
    
    #hailfinder Network
    initHailfinderGraph = Graph("hailfinder.bif")

    hailfinderGraph = copy.deepcopy(initHailfinderGraph)
    print("P (SatContMoist, LLIW | None)")
    hailfinderGraph.getApproximateProbability("SatContMoist, LLIW | None", 60000)

    hailfinderGraph = copy.deepcopy(initHailfinderGraph)
    print("P (SatContMoist, LLIW | RSFcst=XNIL; N32StarFcst=XNIL; MountainFcst=XNIL; AreaMoDryAir=VeryWet)")
    hailfinderGraph.getApproximateProbability("SatContMoist, LLIW | RSFcst=XNIL; N32StarFcst=XNIL; MountainFcst=XNIL; AreaMoDryAir=VeryWet", 60000)

    hailfinderGraph = copy.deepcopy(initHailfinderGraph)
    print("P (SatContMoist, LLIW | RSFcst=XNIL; N32StarFcst=XNIL; MountainFcst=XNIL; AreaMoDryAir=VeryWet; CombVerMo=Down; AreaMeso_ALS=Down; CurPropConv=Strong)")
    hailfinderGraph.getApproximateProbability("SatContMoist, LLIW | RSFcst=XNIL; N32StarFcst=XNIL; MountainFcst=XNIL; AreaMoDryAir=VeryWet; CombVerMo=Down; AreaMeso_ALS=Down; CurPropConv=Strong", 60000)

    #insurance Network
    initInsuranceGraph = Graph("insurance.bif")

    insuranceGraph = copy.deepcopy(initInsuranceGraph)
    print("P (MedCost, ILiCost, PropCost | None)")
    insuranceGraph.getApproximateProbability("MedCost, ILiCost, PropCost | None", 20000)

    insuranceGraph = copy.deepcopy(initInsuranceGraph)
    print("P (MedCost, ILiCost, PropCost | RSFcst=XNIL; N32StarFcst=XNIL; MountainFcst=XNIL; AreaMoDryAir=VeryWet)")
    insuranceGraph.getApproximateProbability("MedCost, ILiCost, PropCost | RSFcst=XNIL; N32StarFcst=XNIL; MountainFcst=XNIL; AreaMoDryAir=VeryWet; CombVerMo=Down; AreaMeso_ALS=Down; CurPropConv=Strong", 20000)

    insuranceGraph = copy.deepcopy(initInsuranceGraph)
    print("P (MedCost, ILiCost, PropCost | Age=Adolescent; GoodStudent=False; SeniorTrain=False; DrivQuality=Poor; MakeModel=Luxury; CarValue=FiftyThou; DrivHistory=Zero)")
    insuranceGraph.getApproximateProbability("MedCost, ILiCost, PropCost | Age=Adolescent; GoodStudent=False; SeniorTrain=False; DrivQuality=Poor; MakeModel=Luxury; CarValue=FiftyThou; DrivHistory=Zero", 20000)
    
    #win95pts Network
    initWin95ptsGraph = Graph("win95pts.bif")

    win95ptsGraph = copy.deepcopy(initWin95ptsGraph)
    print("P (Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | None)")
    win95ptsGraph.getApproximateProbability("Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | None", 16000)

    win95ptsGraph = copy.deepcopy(initWin95ptsGraph)
    print("P (Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem1=No_Output)")
    win95ptsGraph.getApproximateProbability("Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem1=No_Output", 16000)

    win95ptsGraph = copy.deepcopy(initWin95ptsGraph)
    print("P (Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem2=Too_Long)")
    win95ptsGraph.getApproximateProbability("Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem2=Too_Long", 16000)

    win95ptsGraph = copy.deepcopy(initWin95ptsGraph)
    print("P (Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem3=No)")
    win95ptsGraph.getApproximateProbability("Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem3=No", 16000)

    win95ptsGraph = copy.deepcopy(initWin95ptsGraph)
    print("P (Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem4=No)")
    win95ptsGraph.getApproximateProbability("Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem4=No", 16000)

    win95ptsGraph = copy.deepcopy(initWin95ptsGraph)
    print("P (Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem5=No)")
    win95ptsGraph.getApproximateProbability("Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem5=No", 16000)



    win95ptsGraph = copy.deepcopy(initWin95ptsGraph)
    print("P (Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem6=Yes)")
    win95ptsGraph.getApproximateProbability("Problem1, Problem2, Problem3, Problem4, Problem5, Problem6 | Problem6=Yes", 16000)


    print("done")

    