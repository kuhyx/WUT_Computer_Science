import { Test, TestingModule } from '@nestjs/testing';
import { HistoriaZamowienService } from './historia-zamowien.service';

describe('HistoriaZamowienService', () => {
  let service: HistoriaZamowienService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [HistoriaZamowienService],
    }).compile();

    service = module.get<HistoriaZamowienService>(HistoriaZamowienService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
