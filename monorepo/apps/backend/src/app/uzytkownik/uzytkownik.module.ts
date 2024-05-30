import { Module } from '@nestjs/common';
import { UzytkownikService } from './uzytkownik.service';
import { DatabaseModule } from '../database/database.module';
import { DatabaseService } from '../database/database.service';
import { UzytkownikController } from './uzytkownik.controller';

@Module({
  providers: [UzytkownikService, DatabaseService],
  controllers: [UzytkownikController],
})
export class UzytkownikModule {}
