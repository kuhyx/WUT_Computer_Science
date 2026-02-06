// src/zamowione-danie/zamowione-danie.service.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { Zamowione_danie } from '@prisma/client';

@Injectable()
export class ZamowioneDanieService {
  constructor(private prisma: DatabaseService) {}

  async findAll(): Promise<Zamowione_danie[]> {
    return this.prisma.zamowione_danie.findMany();
  }

  async findOne(id: number): Promise<Zamowione_danie | null> {
    return this.prisma.zamowione_danie.findUnique({ where: { id } });
  }

  async create(data: { zamowienieId: number }): Promise<Zamowione_danie> {
    return this.prisma.zamowione_danie.create({ data });
  }

  async update(id: number, data: Partial<Zamowione_danie>): Promise<Zamowione_danie> {
    return this.prisma.zamowione_danie.update({ where: { id }, data });
  }

  async delete(id: number): Promise<Zamowione_danie> {
    return this.prisma.zamowione_danie.delete({ where: { id } });
  }
}
