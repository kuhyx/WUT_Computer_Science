/**
   Unit tests for 2nd EOOP assignment.

   Currency - aggregate 2 doubles (monetary value, exchange rate to dollars)
   CurrencyView - view the given currency with different exchange rate
                  (e.g. view PLN value in GBP), store the reference to the Currency.

   Note that this is in a big part "code reading" exercise.
   Based on this file you should implement two classes mentioned above,
   with proper interface, and in the right header file.

   Make sure that you use proper method composition in your code.

   Please make sure that you compile your solution with warnings enabled and that there are no warnings during compilation. You can do this via the following command:
   g++ -Wall -Wextra -Werror -pedantic lab_2.cpp currency.hpp
 */

#include "currency2.hpp"
#include <iostream>

int main() {
    double monetary_value = 8;
    double usd_exchange_rate = 0.23;

    Currency pln(monetary_value, usd_exchange_rate);

    if (pln.getValue() != 8) {
        std::cerr << "Error in getValue()" << std::endl;
    }
    if (pln.getUSDExchangeRate() != 0.23) {
        std::cerr << pln.getUSDExchangeRate() << std::endl;
        std::cerr << "Error in getUSDExchangeRate()" << std::endl;
    }

    pln.setValue(42);
    pln.setUSDExchangeRate(0.24);
    if (pln.getValue() != 42) {
        std::cerr << "Error in setValue()" << std::endl;
    }
    if (pln.getUSDExchangeRate() != 0.24) {
        std::cerr << "Error in setUSDExchangeRate()" << std::endl;
    }

    Currency gbp(1336, 1.2);
    Currency usd(78, 1);

    if (gbp.toDollars() != 1603.2) {
        std::cerr << "Error in toDollars() 1" << std::endl;
    }
    if (usd.toDollars() != 78) {
        std::cerr << "Error in toDollars() 2" << std::endl;
    }

    gbp.setValueFromDollars(1800);
    usd.setValueFromDollars(120);
    pln.setValueFromDollars(180);
    if (gbp.getValue() != 1500) {
        std::cerr << "Error in setValueFromDollars() 1" << std::endl;
    }
    if (usd.getValue() != 120) {
        std::cerr << "Error in setValueFromDollars() 2" << std::endl;
    }
    if (pln.getValue() != 750) {
        std::cerr << "Error in setValueFromDollars() 3" << std::endl;
    }


    usd.addValue(gbp);
    if (usd.getValue() != 1920) {
        std::cerr << "Error in addValue() 1" << std::endl;
    }
    gbp.addValue(pln);
    if (gbp.getValue() != 1650) {
        std::cerr << "Error in addValue() 2" << std::endl;
    }
    pln.addValue(usd);
    if (pln.getValue() != 8750) {
        std::cerr << "Error in addValue() 3" << std::endl;
    }


    CurrencyView in_gbp(pln, 1.2);
    if (in_gbp.getValue() != 1750) {
        std::cerr << "Error in CurrencyView::getValue() 1" << std::endl;
    }
    pln.setValue(100);
    if (in_gbp.getValue() != 20) {
        std::cerr << "Error in CurrencyView::getValue() 2" << std::endl;
    }


    std::cerr << "End of tests." << std::endl;
    return 0;
}
