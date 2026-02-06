import { Test, TestingModule } from '@nestjs/testing';
import { RestauracjaService } from './restauracja.service';

describe('RestauracjaService', () => {
  let service: RestauracjaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [RestauracjaService],
    }).compile();

    service = module.get<RestauracjaService>(RestauracjaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
