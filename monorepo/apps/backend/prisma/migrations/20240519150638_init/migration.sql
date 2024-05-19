/*
  Warnings:

  - You are about to drop the `HelloWorld` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `example_table` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
DROP TABLE "HelloWorld";

-- DropTable
DROP TABLE "example_table";

-- CreateTable
CREATE TABLE "Restauracja" (
    "id" SERIAL NOT NULL,
    "adres" TEXT NOT NULL,

    CONSTRAINT "Restauracja_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Recencja" (
    "id" SERIAL NOT NULL,
    "tekst" TEXT NOT NULL,
    "wartosc" INTEGER NOT NULL,

    CONSTRAINT "Recencja_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Uzytkownik" (
    "id" SERIAL NOT NULL,
    "imie" TEXT NOT NULL,
    "nazwisko" TEXT NOT NULL,
    "adres" TEXT NOT NULL,

    CONSTRAINT "Uzytkownik_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Historia_zamowien" (
    "id" SERIAL NOT NULL,
    "data_zamowienia" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Historia_zamowien_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Danie" (
    "id" SERIAL NOT NULL,
    "cena" INTEGER NOT NULL,
    "kategoria" TEXT NOT NULL,
    "nazwa" TEXT NOT NULL,

    CONSTRAINT "Danie_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Zamowione_danie" (
    "id" SERIAL NOT NULL,

    CONSTRAINT "Zamowione_danie_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Zamowienie" (
    "id" SERIAL NOT NULL,
    "status" TEXT NOT NULL,

    CONSTRAINT "Zamowienie_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Znizka" (
    "id" SERIAL NOT NULL,
    "kod" TEXT NOT NULL,
    "wartosc" INTEGER NOT NULL,
    "czy_dostepna" BOOLEAN NOT NULL,

    CONSTRAINT "Znizka_pkey" PRIMARY KEY ("id")
);
