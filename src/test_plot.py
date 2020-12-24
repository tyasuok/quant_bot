# obtain all the functions from the file functions.py
from functions_plot import*


# dictionary that will provide data to portfolio's performance graphic 
historic = {'Period':[],
             'Return':[0.02, 0.08, -0.01, -0.02]
    }


# dictionary that will provide data to portfolio's composition plot 
portfolio = {'Stock':['ITUB4','PSSA3','EGIE3'],
             'Amount':[140,60,67],
             'Total Value':[3410.53, 2999.8, 2688.73],
             'Average Value':[]
}
                

# variable to be used in the telegram's function. plot and save the portfolio's composition 
#securities = img_portfolio(portfolio['Total Value'], portfolio['Stock'])

# variable to be used in the telegram's function. plot and save the portfolio's performance
#performance = pic_portfolio_performance(historic["Return"])



                     
                     


#send_image("1496681905:AAGNUmXBHLpXRN4VkcFao1emrBUKW1bRMEs", " composicao ou performance","-356143379" )

