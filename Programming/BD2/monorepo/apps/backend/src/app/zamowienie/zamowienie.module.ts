import { Module } from '@nestjs/common';
import { ZamowienieService } from './zamowienie.service';
import { DatabaseModule } from '../database/database.module';
import { DatabaseService } from '../database/database.service';
import { ZamowienieController } from './zamowienie.controller';

@Module({
  providers: [ZamowienieService, DatabaseService],
  controllers: [ZamowienieController],
})
export class ZamowienieModule {}
