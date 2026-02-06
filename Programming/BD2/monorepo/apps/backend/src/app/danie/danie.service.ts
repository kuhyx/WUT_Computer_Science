import { Injectable } from '@nestjs/common';
import { Danie } from '@prisma/client';
import { DatabaseService } from '../database/database.service';

@Injectable()
export class DanieService {
  constructor(private prisma: DatabaseService) {}

  async findAll(): Promise<Danie[]> {
    return this.prisma.danie.findMany();
  }

  async findOne(id: number): Promise<Danie | null> {
    return this.prisma.danie.findUnique({
      where: { id },
    });
  }

  async create(data: { cena: number; kategoria: string; nazwa: string }): Promise<Danie> {
    return this.prisma.danie.create({
      data,
    });
  }

  async update(id: number, data: Partial<Danie>): Promise<Danie> {
    return this.prisma.danie.update({
      where: { id },
      data,
    });
  }

  async delete(id: number): Promise<Danie> {
    return this.prisma.danie.delete({
      where: { id },
    });
  }
}
