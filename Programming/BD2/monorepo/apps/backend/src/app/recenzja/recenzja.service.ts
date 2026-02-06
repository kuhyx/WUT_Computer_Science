// src/recenzja/recenzja.service.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { Recenzja } from '@prisma/client';

@Injectable()
export class RecenzjaService {
  constructor(private prisma: DatabaseService) {}

  async findAll(): Promise<Recenzja[]> {
    return this.prisma.recenzja.findMany();
  }

  async findOne(id: number): Promise<Recenzja | null> {
    return this.prisma.recenzja.findUnique({ where: { id } });
  }

  async create(data: { tekst: string; wartosc: number; restauracjaId: number; uzytkownikId: number }): Promise<Recenzja> {
    return this.prisma.recenzja.create({ data });
  }

  async update(id: number, data: Partial<Recenzja>): Promise<Recenzja> {
    return this.prisma.recenzja.update({ where: { id }, data });
  }

  async delete(id: number): Promise<Recenzja> {
    return this.prisma.recenzja.delete({ where: { id } });
  }
}
