import { Module } from '@nestjs/common';
import { HistoriaZamowienService } from './historia-zamowien.service';
import { DatabaseModule } from '../database/database.module';
import { DatabaseService } from '../database/database.service';
import { HistoriaZamowienController } from './historia-zamowien.controller';

@Module({
  providers: [HistoriaZamowienService, DatabaseService],
  controllers: [HistoriaZamowienController],
})
export class HistoriaZamowienModule {}
