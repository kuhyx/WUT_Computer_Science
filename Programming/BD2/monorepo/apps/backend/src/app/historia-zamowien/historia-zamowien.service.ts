// src/historia-zamowien/historia-zamowien.service.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { Historia_zamowien } from '@prisma/client';

@Injectable()
export class HistoriaZamowienService {
  constructor(private prisma: DatabaseService) {}

  async findAll(): Promise<Historia_zamowien[]> {
    return this.prisma.historia_zamowien.findMany();
  }

  async findOne(id: number): Promise<Historia_zamowien | null> {
    return this.prisma.historia_zamowien.findUnique({ where: { id } });
  }

  async create(data: { data_zamowienia: Date }): Promise<Historia_zamowien> {
    return this.prisma.historia_zamowien.create({ data });
  }

  async update(id: number, data: Partial<Historia_zamowien>): Promise<Historia_zamowien> {
    return this.prisma.historia_zamowien.update({ where: { id }, data });
  }

  async delete(id: number): Promise<Historia_zamowien> {
    return this.prisma.historia_zamowien.delete({ where: { id } });
  }
}
