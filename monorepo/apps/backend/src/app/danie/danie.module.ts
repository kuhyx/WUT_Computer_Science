import { Module } from '@nestjs/common';
import { DanieService } from './danie.service';
import { DanieController } from './danie.controller';
import { DatabaseService } from '../database/database.service';

@Module({
  providers: [DanieService, DatabaseService],
  controllers: [DanieController],
})
export class DanieModule {}
