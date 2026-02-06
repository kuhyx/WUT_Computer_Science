import { Module } from '@nestjs/common';
import { ZnizkaService } from './znizka.service';
import { DatabaseModule } from '../database/database.module';
import { DatabaseService } from '../database/database.service';
import { ZnizkaController } from './znizka.controller';

@Module({
  providers: [ZnizkaService, DatabaseService],
  controllers: [ZnizkaController],
})
export class ZnizkaModule {}
