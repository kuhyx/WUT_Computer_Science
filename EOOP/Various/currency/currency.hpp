#include <iostream>


class Currency
{
    private:
        double monetary_value;
        double usd_exchange_rate;
    public:
        Currency()
        {
            monetary_value = 0;
            usd_exchange_rate = 1;
        }

        Currency(double value, double rate)
        {
            monetary_value = value;
            usd_exchange_rate = rate;
        }

        double getValue() const { return monetary_value; };

        double getUSDExchangeRate() const { return usd_exchange_rate; };

        void setValue(double value)
        {
            monetary_value = value;
            return;
        };

        void setUSDExchangeRate(double rate)
        {
            usd_exchange_rate = rate;
            return;
        };

        double toDollars() const { return monetary_value * usd_exchange_rate; };

        void setValueFromDollars(double dollarsValue)
        {
            monetary_value = dollarsValue / usd_exchange_rate;
            return;
        }

        void addValue(Currency whichWeAdd)
        {
            monetary_value = (toDollars() + whichWeAdd.toDollars()) / usd_exchange_rate;
        }
};

class CurrencyView
{
    private:
        Currency& original;
        double exchangeRate;
    public:
        CurrencyView(Currency& og, double rate);

        double getValue() const;
};

CurrencyView::CurrencyView(Currency& reference, double rate) : original(reference)
{
    exchangeRate = rate;
}

double CurrencyView::getValue() const
{
    return original.toDollars() / exchangeRate;
}

