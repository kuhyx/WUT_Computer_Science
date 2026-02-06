import { Module } from '@nestjs/common';
import { RestauracjaService } from './restauracja.service';
import { DatabaseModule } from '../database/database.module';
import { DatabaseService } from '../database/database.service';
import { RestauracjaController } from './restauracja.controller';

@Module({
  providers: [RestauracjaService, DatabaseService],
  imports: [DatabaseModule],
  controllers: [RestauracjaController],
})
export class RestauracjaModule {}
