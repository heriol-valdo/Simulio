import pandas as pd
import numpy as np
import numpy_financial
import datetime


def CalculerMensualité39_bis2_ANCIEN(N, C2, T, ASSU, apport, mois, annee, fraisAgence, fraisNotaire, TRAVAUX, revalorisationBien):

    CDEPART = C2
    fraisAgence2 = (fraisAgence/100) * C2
    fraisNotaire_val = (fraisNotaire/100) * C2
    C2 = C2 - apport
    garantieBancaire = (1.5/100)*C2
    if  garantieBancaire <0:
        garantieBancaire = 0
    else :
        garantieBancaire = garantieBancaire
    if  fraisAgence2 <0:
        fraisAgence2 = 0
    else :
        fraisAgence2 = fraisAgence2

    C2 = C2 + fraisNotaire_val + garantieBancaire + fraisAgence2 + TRAVAUX
    N2 = N
    N = N * 12
    t = T / 12
    q = 1 + t / 100  # calcul du coefficient multiplicateur associé à une hausse de t%
    M = (q**N * C2 * (1 - q) / (1 - q**N)) + C2*((ASSU/100)/12)
    A = C2*((ASSU/100))*(N/12)
    I = N * M - C2  # calcul des intérêts versés
    T2 = T * 1 / 100
    date = "{}/01/{}".format(mois,annee)
    rng = pd.date_range(start=date, periods=N, freq='MS')
    rng.name = "Date"
    df = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name = "Mois"

    df["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, C2) + C2 * ((ASSU/100)/12)
    df["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12, df.index,N, C2)
    df["Intérêts"] = -1 * numpy_financial.ipmt(T2 / 12, df.index, N, C2)
    df = df.round(2)

    df["Capital restant dû"] = 0.0
    df.loc[1, "Capital restant dû"] = float(C2 - df.loc[1, "Capital Amorti"])

    for period in range(2, len(df) + 1):
        previous_balance = df.loc[period-1, "Capital restant dû"]
        principal_paid = df.loc[period, "Capital Amorti"]

        if previous_balance == 0:
            df.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] = 0
            continue
        elif principal_paid <= previous_balance:
            df.loc[period, "Capital restant dû"] = previous_balance - principal_paid

    df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")

    salaireMinimum = (M*100)/35
    salaireMinimum = int(salaireMinimum)
    

    if M < 0:
        M=0
    else :
        M=M
    
    if salaireMinimum < 0:
        salaireMinimum = 0
    else :
        salaireMinimum = salaireMinimum

    if C2 < 0:
        C2 = 0
    else :
        C2 = C2
    
    
    data = {
    "Prix du bien": CDEPART,
    'Frais de notaire': fraisNotaire_val,
    'Garantie Bancaire': garantieBancaire,
    "Frais d'agence": fraisAgence2,
    "Apport": apport,
    "Total à financer": C2
    }

    # Créez un DataFrame à partir du dictionnaire
    output2 = pd.DataFrame([data])

    #print(output2)

    data2 = {
    "Montant du prêt total": C2,
    "Taux d'intérêt": T,
    "Taux d'assurance": ASSU,
    "Mensualité de crédit": df["Mensualité"].iloc[0],
    }
    output3 = pd.DataFrame([data2])

    date_initiale = datetime.datetime.strptime("{}/01/{}".format(mois,annee), "%m/%d/%Y")

    # Ajouter 25 ans

    date_finale = date_initiale.replace(year=date_initiale.year + N2)
    # Formater la date finale
    date_finale_str = date_finale.strftime("%d/%m/%Y")

    data3 = {
    "Date d'acquisition": date,
    "Fin du financement": date_finale_str,
    }
    output4 = pd.DataFrame([data3])
    #print(output4)


    liste_prixdubien = []
    prixDuBien2 = CDEPART
    listeprixdubieninitial = [prixDuBien2]
    for year in range(1, int(N/12)+1):
        prixDuBien2 *= (1+revalorisationBien/100)
        liste_prixdubien.append(prixDuBien2)
    listeprixdubieninitial.extend(liste_prixdubien)

    #print(len(listeprixdubieninitial))

    nbreAnnees = int(N / 12)
    liste_annee = [date_initiale.year + i for i in range(nbreAnnees + 1)]

    df_somme = pd.DataFrame(
    {
    'Prix du bien': listeprixdubieninitial,
    "Date": liste_annee,
    })
    #print(df_somme)
    df_somme["Periode (en années)"] = df_somme["Date"].astype(str)


    df['Year'] = pd.to_datetime(df["Date"], format='%d/%m/%Y').dt.year

    # Créez le dictionnaire de mappage avec les années
    products_dict = dict(zip(df.Year, df["Capital restant dû"]))

    # Utilisez le dictionnaire pour mettre à jour df_somme
    df_somme["Capital restant dû"] = df_somme["Date"].map(products_dict).fillna(0).replace([float('inf'), -float('inf')], 0)
    df_somme["Somme disponible en cas de revente"] = df_somme["Prix du bien"] - df_somme["Capital restant dû"]

    df_somme = df_somme.set_index("Periode (en années)")
    output13 = df_somme.drop(columns="Date")


    for col in output4.columns:
        output4[col] = output4[col].astype(str)

    # Convertir tous les DataFrames en dicts JSON-compatibles
    df= df.to_dict(orient="records")
    output2 = output2.to_dict(orient="records")
    output3 = output3.to_dict(orient="records")
    output4 = output4.to_dict(orient="records")
    output13 =output13.reset_index().to_dict(orient="records")

   

    return M,I,A,fraisNotaire_val,garantieBancaire,salaireMinimum,df,fraisAgence2,C2,output2,output3,output4,output13,TRAVAUX


#print(CalculerMensualité39_bis2_ANCIEN(25,200000,4,0.3,0,"02","2025",3,2.5,0,1))
