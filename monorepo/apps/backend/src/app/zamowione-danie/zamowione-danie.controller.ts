// src/zamowione-danie/zamowione-danie.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { ZamowioneDanieService } from './zamowione-danie.service';
import { Zamowione_danie } from '@prisma/client';

@Controller('zamowione-danie')
export class ZamowioneDanieController {
  constructor(private readonly zamowioneDanieService: ZamowioneDanieService) {}

  @Get()
  async findAll(): Promise<Zamowione_danie[]> {
    return this.zamowioneDanieService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Zamowione_danie | null> {
    return this.zamowioneDanieService.findOne(+id);
  }

  @Post()
  async create(@Body() data: { zamowienieId: number }): Promise<Zamowione_danie> {
    return this.zamowioneDanieService.create(data);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Zamowione_danie>): Promise<Zamowione_danie> {
    return this.zamowioneDanieService.update(+id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<Zamowione_danie> {
    return this.zamowioneDanieService.delete(+id);
  }
}
