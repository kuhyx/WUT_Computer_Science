import { Test, TestingModule } from '@nestjs/testing';
import { UzytkownikService } from './uzytkownik.service';

describe('UzytkownikService', () => {
  let service: UzytkownikService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [UzytkownikService],
    }).compile();

    service = module.get<UzytkownikService>(UzytkownikService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
