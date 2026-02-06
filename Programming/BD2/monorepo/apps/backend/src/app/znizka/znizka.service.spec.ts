import { Test, TestingModule } from '@nestjs/testing';
import { ZnizkaService } from './znizka.service';

describe('ZnizkaService', () => {
  let service: ZnizkaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ZnizkaService],
    }).compile();

    service = module.get<ZnizkaService>(ZnizkaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
