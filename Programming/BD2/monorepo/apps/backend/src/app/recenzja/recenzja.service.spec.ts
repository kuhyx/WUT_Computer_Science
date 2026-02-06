import { Test, TestingModule } from '@nestjs/testing';
import { RecenzjaService } from './recenzja.service';

describe('RecenzjaService', () => {
  let service: RecenzjaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [RecenzjaService],
    }).compile();

    service = module.get<RecenzjaService>(RecenzjaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
