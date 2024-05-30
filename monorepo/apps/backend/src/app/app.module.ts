import { Module } from '@nestjs/common';

import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DatabaseModule } from './database/database.module';
import { RestauracjaModule } from './restauracja/restauracja.module';
import { RecenzjaModule } from './recenzja/recenzja.module';
import { UzytkownikModule } from './uzytkownik/uzytkownik.module';
import { HistoriaZamowienModule } from './historia-zamowien/historia-zamowien.module';
import { DanieModule } from './danie/danie.module';
import { ZamowioneDanieModule } from './zamowione-danie/zamowione-danie.module';
import { ZamowienieModule } from './zamowienie/zamowienie.module';
import { ZnizkaModule } from './znizka/znizka.module';

@Module({
  imports: [
    DatabaseModule,
    RestauracjaModule,
    RecenzjaModule,
    UzytkownikModule,
    HistoriaZamowienModule,
    DanieModule,
    ZamowioneDanieModule,
    ZamowienieModule,
    ZnizkaModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
