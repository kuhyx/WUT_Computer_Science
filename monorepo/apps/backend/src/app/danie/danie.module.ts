import { Module } from '@nestjs/common';
import { DanieService } from './danie.service';
import { DanieController } from './danie.controller';

@Module({
  providers: [DanieService],
  controllers: [DanieController],
})
export class DanieModule {}
