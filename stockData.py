import yfinance as yf
import pandas as pd

#Haettavat yritykset
yritykset = ["NOKIA.HE", "FORTUM.HE", "TIETO.HE", "KCR.HE"]

#Listat tietojen tallennukseen
paikkatiedot = []
historiatiedot = []
taloustiedot = []
sulkutieto = []

for symbol in yritykset:
    yritys = yf.Ticker(symbol)

    #Yritystiedot
    yritystieto = yritys.info
    paikkatieto = {
        'Company Symbol': symbol,
        'Company Name': yritystieto.get("longName", "N/A"),
        'Headquarters Location': yritystieto.get("address1", "N/A"),
        'City': yritystieto.get("city", "N/A"),
        'Country': yritystieto.get("country", "N/A")
    }
    paikkatiedot.append(paikkatieto)

    #Historia data
    history_data = yritys.history()
    history_data['Date'] = history_data.index  
    history_data['Company Symbol'] = symbol  
    historiatiedot.append(history_data)

    #Talousdata
    financials_data = yritys.financials.reset_index().rename(columns={'index': 'Year'})
    financials_data['Company Symbol'] = symbol 
    taloustiedot.append(financials_data)

    #Sulkemistiedot
    historia = history_data['Close'][0]
    sulkutieto.append({'Company Symbol': symbol, 'Close': historia})


#Luo dataframet listoista
df_locations = pd.DataFrame(paikkatiedot)
df_histories = pd.concat(historiatiedot)
df_financials = pd.concat(taloustiedot)
df_sulku = pd.DataFrame(sulkutieto)


#Tulosta dataframet
print("Location Data:")
print(df_locations)

print("\nHistorical Data:")
for symbol, df in df_histories.items():
    print(f"Company: {symbol}")
    print(df)

print("\nFinancial Data:")
for symbol, df in df_financials.items():
    print(f"Company: {symbol}")
    print(df)

print("\nTesti Data:")
print(df_sulku)
