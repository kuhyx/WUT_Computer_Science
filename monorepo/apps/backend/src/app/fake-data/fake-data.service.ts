import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { faker } from '@faker-js/faker';

@Injectable()
export class FakeDataService {
  constructor(private prisma: DatabaseService) {}

  async generateFakeData() {
    // Generate fake Restauracja
    for (let i = 0; i < 10; i++) {
      await this.prisma.restauracja.create({
        data: {
          adres: faker.location.streetAddress(),
        },
      });
    }

    // Generate fake Uzytkownik and Historia_zamowien
    for (let i = 0; i < 10; i++) {
      const historia = await this.prisma.historia_zamowien.create({
        data: {
          data_zamowienia: faker.date.past(),
        },
      });

      await this.prisma.uzytkownik.create({
        data: {
          imie: faker.person.firstName(),
          nazwisko: faker.person.lastName(),
          adres: faker.location.streetAddress(),
          Historia_zamowienId: historia.id,
        },
      });
    }

    // Generate fake Danie
    for (let i = 0; i < 10; i++) {
      await this.prisma.danie.create({
        data: {
          cena: faker.number.int({ min: 10, max: 100 }),
          kategoria: faker.commerce.department(),
          nazwa: faker.commerce.productName(),
        },
      });
    }

    // Generate fake Zamowienie and Zamowione_danie
    for (let i = 0; i < 10; i++) {
      const zamowienie = await this.prisma.zamowienie.create({
        data: {
          status: faker.helpers.arrayElement(['Pending', 'Completed', 'Cancelled']),
        },
      });

      await this.prisma.zamowione_danie.create({
        data: {
          zamowienieId: zamowienie.id,
        },
      });
    }

    // Generate fake Znizka
    for (let i = 0; i < 10; i++) {
      const restauracja = await this.prisma.restauracja.findFirst();
      await this.prisma.znizka.create({
        data: {
          kod: faker.string.alphanumeric(10),
          wartosc: faker.number.int({ min: 10, max: 50 }),
          czy_dostepna: faker.datatype.boolean(),
          restauracjaId: restauracja.id,
        },
      });
    }

    // Generate fake Recenzja
    for (let i = 0; i < 10; i++) {
      const restauracja = await this.prisma.restauracja.findFirst();
      const uzytkownik = await this.prisma.uzytkownik.findFirst();
      await this.prisma.recenzja.create({
        data: {
          tekst: faker.lorem.sentences(),
          wartosc: faker.number.int({ min: 1, max: 5 }),
          restauracjaId: restauracja.id,
          uzytkownikId: uzytkownik.id,
        },
      });
    }
  }
}
