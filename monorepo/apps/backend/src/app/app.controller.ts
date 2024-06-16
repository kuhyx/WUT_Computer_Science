import { Controller, Get } from '@nestjs/common';

import { AppService } from './app.service';
import { FakeDataService } from './fake-data/fake-data.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService,
    private readonly fakeDataService: FakeDataService
  ) {}

  @Get('generate-fake-data')
  async generateFakeData() {
    await this.fakeDataService.generateFakeData();
    return { message: 'Fake data generated successfully' };
  }

  @Get()
  getData() {
    return this.appService.getData();
  }
}
