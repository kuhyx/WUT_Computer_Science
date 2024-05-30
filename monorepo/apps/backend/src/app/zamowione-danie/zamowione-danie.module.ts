import { Module } from '@nestjs/common';
import { ZamowioneDanieService } from './zamowione-danie.service';
import { DatabaseModule } from '../database/database.module';
import { DatabaseService } from '../database/database.service';
import { ZamowioneDanieController } from './zamowione-danie.controller';

@Module({
  providers: [ZamowioneDanieService, DatabaseService],
  controllers: [ZamowioneDanieController],
})
export class ZamowioneDanieModule {}
