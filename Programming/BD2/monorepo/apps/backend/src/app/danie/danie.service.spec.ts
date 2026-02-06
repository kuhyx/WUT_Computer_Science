import { Test, TestingModule } from '@nestjs/testing';
import { DanieService } from './danie.service';

describe('DanieService', () => {
  let service: DanieService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [DanieService],
    }).compile();

    service = module.get<DanieService>(DanieService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
