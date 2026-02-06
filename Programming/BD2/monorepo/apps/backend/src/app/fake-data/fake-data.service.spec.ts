import { Test, TestingModule } from '@nestjs/testing';
import { FakeDataService } from './fake-data.service';

describe('FakeDataService', () => {
  let service: FakeDataService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [FakeDataService],
    }).compile();

    service = module.get<FakeDataService>(FakeDataService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
