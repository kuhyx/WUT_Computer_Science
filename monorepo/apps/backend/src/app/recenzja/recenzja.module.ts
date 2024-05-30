import { Module } from '@nestjs/common';
import { RecenzjaService } from './recenzja.service';
import { DatabaseModule } from '../database/database.module';
import { DatabaseService } from '../database/database.service';
import { RecenzjaController } from './recenzja.controller';

@Module({
  providers: [RecenzjaService, DatabaseService],
  exports: [RecenzjaService],
  controllers: [RecenzjaController],
})
export class RecenzjaModule {}
